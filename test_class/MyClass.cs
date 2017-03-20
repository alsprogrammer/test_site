/*
 * Created by SharpDevelop.
 * User: Александр
 * Date: 20.03.2017
 * Time: 11:26
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Xml;
using System.Drawing;

namespace TestClass
{
    /// <summary>
    /// Класс для работы с изображениями в тесте.
    /// </summary>
    public class TestImage
    {
        /// <summary>
        /// Преобразует строку в изображение
        /// </summary>
        /// <param name="Encoded">строка, содержащая картинку</param>
        /// <returns></returns>
        public static Image ImageFromString(string Encoded)
        {
            Image Ret = null;

            if (!String.IsNullOrEmpty(Encoded))
            {
                try
                {
                    MemoryStream ms = new MemoryStream();
                    byte[] bImage = Convert.FromBase64String(Encoded);
                    ms.Write(bImage, 0, bImage.GetLength(0));
                    Ret = System.Drawing.Bitmap.FromStream(ms);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось преобразовать строку в изображение: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задана строка, из которой должно быть получено изображение");

            return Ret;
        }

        /// <summary>
        /// Преобразует изображение в строку
        /// </summary>
        /// <param name="Image">изображение</param>
        /// <returns></returns>
        public static string StringFromImage(Image Image)
        {
            string sRet = null;

            if (Image != null)
            {
                try
                {
                    MemoryStream ms = new MemoryStream();
                    Image.Save(ms, System.Drawing.Imaging.ImageFormat.Png);

                    sRet = Convert.ToBase64String(ms.ToArray());
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось преобразовать изображение  в строку: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задано изображение, из которого должна быть получена строка");

            return sRet;
        }

        /// <summary>
        /// Читает изображение из xml-узла
        /// </summary>
        /// <param name="QImage">Узел, содержащий изображение</param>
        /// <param name="Parent">объект, из которого берется узел, нужен для вытаскивания пути к файлу изображения, если его нет в виде текстовой строки</param>
        /// <returns>System.Drawing.Bitmap</returns>
        public static Image ImageFromXmlNode(XmlNode QImage, BaseObject Parent)
        {
            Image Ret = null;

            if (QImage != null && Parent != null)
            {
                try
                {
                    if (!String.IsNullOrEmpty(QImage.InnerText))
                    {
                        Ret = ImageFromString(QImage.InnerText);
                    }
                    else
                    {
                        string sFileName = null;
                        try
                        {
                            if (Parent.SourceFile != null)
                                sFileName = Parent.SourceFile.Directory.FullName + "\\" + QImage.Attributes["filename"].Value;
                        }
                        catch
                        {
                            sFileName = null;
                        }
                        if (!String.IsNullOrEmpty(sFileName))
                        {
                            if (System.IO.File.Exists(sFileName))
                                Ret = System.Drawing.Bitmap.FromFile(sFileName);
                        }
                    }
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось выделить изображение из xml-узла: " + e1.Message, e1);
                }
            }

            return Ret;
        }
    }

    public class TimesUpException : Exception
    {
    }

    interface ITestObject
    {
        XmlNode ExportToXmlNode(XmlDocument Document);
        void LoadFromXmlNode(XmlNode Node);
        void SaveToXmlStream(Stream Stream);
        void LoadFromXmlStream(Stream Stream);
        void SaveToXmlFile(string FileName);
        void LoadFromXmlFile(string FileName);
    }

    public abstract class BaseObject:ITestObject
    {
        protected FileInfo File = null;
        protected Random rnd = new Random(DateTime.Now.Millisecond);

        public FileInfo SourceFile
        {
            get { return File; }
        }
        
        #region ITestObject Members

        public abstract XmlNode ExportToXmlNode(XmlDocument Document);
        public abstract void LoadFromXmlNode(XmlNode Node);

        public virtual void SaveToXmlStream(Stream Stream)
        {
            if (Stream != null)
            {
                XmlDocument WriteDoc = new XmlDocument();
                XmlNode ExportNode = ExportToXmlNode(WriteDoc);
                if (ExportNode != null)
                {
                    try
                    {
                        XmlDeclaration Decl = WriteDoc.CreateXmlDeclaration("1.0", "utf-8", null);
                        WriteDoc.AppendChild(Decl);
                        WriteDoc.AppendChild(ExportNode);
                        WriteDoc.Save(Stream);

                        File = null;
                    }
                    catch (Exception e1)
                    {
                        throw new Exception("Ошибка при попытке экспорта в Xml-поток:" + e1.Message, e1);
                    }
                }
                else
                    throw (new Exception("Не удалось получить Xml-документ, соответствующий объекту"));
            }
            else
                throw (new Exception("Попытка записать в несуществующий поток"));
        }

        public virtual void LoadFromXmlStream(Stream Stream)
        {
            if (Stream!=null)
            {
                try
                {
                    XmlDocument MainDoc = new XmlDocument();
                    MainDoc.Load(Stream);
                    XmlNode GlobalNode = MainDoc.FirstChild;
                    LoadFromXmlNode(GlobalNode);

                    File = null;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось считать входной файл:" + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указано имя входного файла");
        }

        /// <summary>
        /// Сохраняет объект в xml-файл.
        /// Внимание! Проверьте метод SaveToXmlStream для проверки, что именно будет сохранено!
        /// </summary>
        /// <param name="FileName"></param>
        public virtual void SaveToXmlFile(string FileName)
        {
            if (!String.IsNullOrEmpty(FileName))
            {
                try
                {
                    FileStream fs = new FileStream(FileName, FileMode.CreateNew);
                    SaveToXmlStream(fs);
                    fs.Flush();
                    File = new FileInfo(FileName);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось сохранить объект в файл: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указано имя выходного файла");
        }

        public virtual void LoadFromXmlFile(string FileName)
        {
            if (!String.IsNullOrEmpty(FileName))
            {
                try
                {
                    XmlDocument MainDoc = new XmlDocument();
                    MainDoc.Load(FileName);
                    XmlNode GlobalNode=MainDoc.FirstChild;
                    LoadFromXmlNode(GlobalNode);
                    File = new FileInfo(FileName);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось считать входной файл:" + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указано имя входного файла");
        }

        #endregion
    }
    
    /// <summary>
    /// Описывает студента.
    /// </summary>
    public class Student:BaseObject
    {
        protected string sFirstName = null;
        protected string sMiddleName = null;
        protected string sLastName = null;

        protected Group StudentGroup = null;

        /// <summary>
        /// Имя студента
        /// </summary>
        public string Name
        {
            get { return sFirstName + " " + sMiddleName + " " + sLastName; }
        }

        /// <summary>
        ///  Группа студента
        /// </summary>
        public Group Group
        {
            get { return StudentGroup; }
        }

        /// <summary>
        /// Создание студента
        /// </summary>
        /// <param name="FirstName">Имя</param>
        /// <param name="MiddleName">Отчество</param>
        /// <param name="LastName">Фамилия</param>
        /// <param name="StudentGroup">Группа студента</param>
        public Student(string FirstName, string MiddleName, string LastName, Group StudentGroup)
        {
            if (!String.IsNullOrEmpty(FirstName) && !String.IsNullOrEmpty(MiddleName) && !String.IsNullOrEmpty(LastName) && StudentGroup != null)
            {
                this.StudentGroup = StudentGroup;
                sFirstName = FirstName;
                sMiddleName = MiddleName;
                sLastName = LastName;
            }
            else
                throw new Exception("Не указаны имя, фамилия или отчетсво студента, либо его группа");
        }

        /// <summary>
        /// создает студента из xml-узла
        /// </summary>
        /// <param name="StudentNode">Узел</param>
        /// <param name="StudentGroup">Группа студента</param>
        public Student(XmlNode StudentNode, Group StudentGroup)
        {
            if (StudentNode != null && StudentGroup != null)
            {
                this.StudentGroup = StudentGroup;
                LoadFromXmlNode(StudentNode);
            }
            else
                throw new Exception("Не указана группа студента или xml-узел");
        }

        /// <summary>
        /// Экспортирует в xml-узел
        /// </summary>
        /// <param name="Document">Документ, в который экспортируется узел</param>
        /// <returns>Узел</returns>
        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            XmlElement StudNode = null;
            if (Document != null)
            {
                try
                {
                    StudNode = Document.CreateElement("Student");

                    XmlElement StudFN = Document.CreateElement("FirstName");
                    XmlText FNameTxt = Document.CreateTextNode(sFirstName);
                    StudFN.AppendChild(FNameTxt);
                    StudNode.AppendChild(StudFN);

                    XmlElement StudMN = Document.CreateElement("MiddleName");
                    XmlText MNameTxt = Document.CreateTextNode(sMiddleName);
                    StudMN.AppendChild(MNameTxt);
                    StudNode.AppendChild(StudMN);

                    XmlElement StudLN = Document.CreateElement("LastName");
                    XmlText LNameTxt = Document.CreateTextNode(sLastName);
                    StudLN.AppendChild(LNameTxt);
                    StudNode.AppendChild(StudLN);
                }
                catch (Exception e1)
                {
                    throw new Exception(String.Format("Не удалось прочитать студента из XML-узла", e1.Message), e1);
                }

                return StudNode;
            }
            else
                throw new Exception("Не задан документ, для которого необходимо создать узел");
        }

        /// <summary>
        /// Загружает из xml-узла.
        /// Внимание! Группа студента в объекте студент - не меняется!
        /// </summary>
        /// <param name="Node">Узел, из которго происходит загрузка</param>
        public override void LoadFromXmlNode(XmlNode Node)
        {
            if (Node != null)
            {
                try
                {
                    sFirstName = Node["FirstName"].InnerText;
                    sMiddleName = Node["MiddleName"].InnerText;
                    sLastName = Node["LastName"].InnerText;
                }
                catch(Exception e1)
                {
                    throw new Exception("не удалось получить данные из xml-узла студента: "+e1.Message, e1);
                }
            }
            else
                throw new Exception("не указан xml-узел, из которого будет осуществлена загрузка студента");
        }

        /// <summary>
        /// Сохраняет в xml-поток. 
        /// Внимание! Сохраняется так же информация о группе студента!
        /// </summary>
        /// <param name="Stream">Поток</param>
        public override void SaveToXmlStream(Stream Stream)
        {
            XmlDocument Doc = new XmlDocument();
            XmlElement StudNode = Doc.CreateElement("Student");

            StudNode.AppendChild(StudentGroup.ExportToXmlNode(Doc));
            StudNode.AppendChild(this.ExportToXmlNode(Doc));

            Doc.AppendChild(StudNode);

            Doc.Save(Stream);
        }

        public override string ToString()
        {
            return sLastName + " " + sFirstName + " " + sMiddleName;
        }
    }

    /// <summary>
    /// Описывает учебную группу
    /// </summary>
    public class Group:BaseObject
    {
        protected string sGroupName = null;
        protected string sSpeciality = null;
        protected int iLearningStartYear = -1;
        protected List<Student> GroupStudents = null;

        /// <summary>
        /// Название группы
        /// </summary>
        public string Name
        {
            get { return sGroupName; }
        }
        /// <summary>
        /// специальность, по которой обучается группа
        /// </summary>
        public string Speciality
        {
            get { return sSpeciality; }
        }
        /// <summary>
        /// Год начала обучения
        /// </summary>
        public int StartYear
        {
            get { return iLearningStartYear; }
        }

        /// <summary>
        /// Студент из группы с заданным номером
        /// </summary>
        /// <param name="iStudentNum"></param>
        /// <returns></returns>
        public Student this[int iStudentNum]
        {
            get { if (iStudentNum >= 0 && iStudentNum < GroupStudents.Count) return GroupStudents[iStudentNum]; else throw new Exception("Неверно указан номер студента"); }
        }

        /// <summary>
        /// Добавляет студента в группу
        /// </summary>
        /// <param name="NewStudent"></param>
        public void AddStudent(Student NewStudent)
        {
            if (NewStudent != null)
            {

                if (NewStudent.Group == this)
                {
                    try
                    {
                        GroupStudents.Add(NewStudent);
                    }
                    catch (Exception e1)
                    {
                        throw new Exception(String.Format("Не удалось добавить студента: {0}", e1.Message), e1);
                    }
                }
                else
                    throw new Exception("Нельзя добавить в данную группу студента из другой группы");
            }
            else
                throw new Exception("попытка добавить неопределенного студента");
        }

        /// <summary>
        /// Удаляет студента с заданным номером
        /// </summary>
        /// <param name="iStudentNum"></param>
        public void RemoveStudentAt(int iStudentNum)
        {
            if (iStudentNum >= 0 && iStudentNum < GroupStudents.Count)
            {
                try
                {
                    GroupStudents.RemoveAt(iStudentNum);
                }
                catch (Exception e1)
                {
                    throw new Exception(String.Format("Не удалось удалить студента: {0}", e1.Message), e1);
                }
            }
            else
                throw new Exception("Нет студента с таким номером");
        }

        /// <summary>
        /// Удаляет заданного студента
        /// </summary>
        /// <param name="iStudentNum"></param>
        public void RemoveStudentAt(Student StudentToRemove)
        {
            if (StudentToRemove!=null)
            {
                try
                {
                    GroupStudents.Remove(StudentToRemove);
                }
                catch (Exception e1)
                {
                    throw new Exception(String.Format("Не удалось удалить студента: {0}", e1.Message), e1);
                }
            }
            else
                throw new Exception("Студент не задан.");
        }

        /// <summary>
        /// Создает группу по названию, специальности и году начала обучения
        /// </summary>
        /// <param name="Name"></param>
        /// <param name="Speciality"></param>
        /// <param name="StartYear"></param>
        public Group(string Name, string Speciality, int StartYear)
        {
            if (!String.IsNullOrEmpty(Name) && !String.IsNullOrEmpty(Speciality) && StartYear > 1990 && StartYear < 2050)
            {
                sGroupName = Name;
                sSpeciality = Speciality;
                iLearningStartYear = StartYear;
                GroupStudents = new List<Student>();
            }
            else
                throw new Exception("Попытка создать группу с неправильным названием, спеиальностью или годом обучения");
        }

        /// <summary>
        /// Создает группу из xml-узла
        /// </summary>
        /// <param name="GroupNode"></param>
        public Group(XmlNode GroupNode)
        {
            if (GroupNode!=null)
            {
                LoadFromXmlNode(GroupNode);
            }
            else
                throw new Exception("Попытка создать группу из пустого xml-узла");
        }

        /// <summary>
        /// Сохраняет группу в xml-узел
        /// </summary>
        /// <param name="Document"></param>
        /// <returns></returns>
        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            XmlElement GroupNode = null;
            if (Document != null)
            {
                try
                {
                    GroupNode = Document.CreateElement("Group");
                    XmlAttribute Spec = Document.CreateAttribute("speciality");
                    Spec.Value = sSpeciality;
                    GroupNode.Attributes.Append(Spec);

                    XmlElement GName = Document.CreateElement("Name");
                    XmlText GNameTxt = Document.CreateTextNode(sGroupName);
                    GName.AppendChild(GNameTxt);
                    GroupNode.AppendChild(GName);

                    XmlElement StartY = Document.CreateElement("StartYear");
                    XmlText StartYTxt = Document.CreateTextNode(Convert.ToString(iLearningStartYear));
                    StartY.AppendChild(StartYTxt);
                    GroupNode.AppendChild(StartY);

                    XmlElement StudentsElem = Document.CreateElement("Students");
                    foreach (Student CurStudent in GroupStudents)
                        StudentsElem.AppendChild(CurStudent.ExportToXmlNode(Document));
                }
                catch (Exception e1)
                {
                    throw new Exception(String.Format("Не удалось сохранить группу в XML-узел: {0}", e1.Message),e1);
                }

                return GroupNode;
            }
            else
                throw new Exception("Не указан документ, к которому необходимо дабавить узел");
        }

        /// <summary>
        /// Считывает информацию о группе из xml-узла
        /// </summary>
        /// <param name="Node"></param>
        public override void LoadFromXmlNode(XmlNode Node)
        {
            if (Node != null)
            {
                try
                {
                    sSpeciality = Node.Attributes["speciality"].Value;
                    sGroupName = Node["Name"].InnerText;
                    iLearningStartYear = Convert.ToInt32(Node["StartYear"].InnerText);
                    XmlNodeList StudentNodes = Node.SelectNodes("Students");
                    foreach (XmlNode CurStudentNode in StudentNodes)
                        GroupStudents.Add(new Student(CurStudentNode, this));
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось прочитать группу из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан узел, из которого будет загружена группа");
        }

        /// <summary>
        /// Сохраняет группу в xml-поток
        /// </summary>
        /// <param name="Stream"></param>
        public override void SaveToXmlStream(Stream Stream)
        {
            XmlDocument Doc = new XmlDocument();
            Doc.AppendChild(this.ExportToXmlNode(Doc));

            Doc.Save(Stream);
        }

        public override string ToString()
        {
            return String.Format("{0} ({1}, {2})", sGroupName, iLearningStartYear, sSpeciality);
        }
    }

    public abstract class CommonTest:BaseObject
    {
        protected DateTime CreateDateTime;
        protected string sName = null;
        protected string sSpecialityName = null;
        protected string sDiscipline = null;
        protected int nSecondsToTest = -1;

        public DateTime DateTime
        {
            get { return CreateDateTime; }
        }
        public string Name
        {
            get { return sName; }
        }
        public string SpecialityName
        {
            get { return sSpecialityName; }
        }
        public abstract int QuestionNumber
        {
            get;
        }
        public abstract CommonQuestion this[int QuestionIndex]
        {
            get;
        }
        public int Duration
        {
            get { return nSecondsToTest; }
        }
        
        public abstract void AddQuestion(CommonQuestion Question);
        public abstract void RemoveQuestion(int QuestionNumber);
        public abstract void RemoveQuestion(CommonQuestion Question);

        public override string ToString()
        {
            return sName;
        }
    }

    abstract public class CommonQuestion:BaseObject
    {
        protected CommonTest ParentTest = null;
        
        protected string sText = null;
        protected string sThemeName = null;
        protected Image QuestionImage = null;

        public CommonTest Test
        {
            get { return ParentTest; }
        }
        public string Text
        {
            get { return sText; }
        }
        public string ThemeName
        {
            get { return sThemeName; }
        }
        public Image Image
        {
            get { return QuestionImage; }
            set { QuestionImage = value; }
        }
        public abstract int VariantNumber
        {
            get;
        }

        public abstract void AddVariant(CommonAnswerVariant Variant);
        public abstract void RemoveVariant(int VariantNumber);
        public abstract void RemoveVariant(CommonAnswerVariant Variant);
        public abstract CommonAnswerVariant this[int AnswerVariantIndex]
        {
            get;
        }
    }

    abstract public class CommonAnswerVariant:BaseObject
    {
        protected CommonQuestion ParentQuestion = null;
        protected string sText = null;
        protected Image VariantImage = null;
        protected bool blRight = false;

        public CommonQuestion Question
        {
            get { return ParentQuestion; }
        }
        public string Text
        {
            get { return sText; }
        }
        public Image Image
        {
            get { return VariantImage; }
            set { VariantImage = value; }
        }
        public bool Right
        {
            get { return blRight; }
        }
    }

    /// <summary>
    /// Полный тест по дисциплине, включающий все вопросы.
    /// Можно сохранять в xml-файл.
    /// </summary>
    public class WholeTest : CommonTest
    {
        protected List<WholeTestQuestion> Questions = null;

        public WholeTest(StreamReader sr)
        {
            if (sr != null)
            {
                ReadFromStream(sr);
                File = null;
            }
            else throw new Exception("Попытка считать тест из пустого потока");
        }

        public WholeTest(string FileName)
        {
            if (System.IO.File.Exists(FileName))
            {
                ReadFromStream(new StreamReader(FileName));
                File = new FileInfo(FileName);
            }
            else
                throw new Exception("Не существует файл:" + FileName);
        }
        
        /// <summary>
        /// 
        /// </summary>
        /// <param name="Name">Название теста</param>
        /// <param name="Speciality">Специальность</param>
        /// <param name="Discipline">Дисциплина</param>
        /// <param name="DurationInSeconds">Продолжительность теста в секундах, -1 - не ограничена</param>
        public WholeTest(string Name, string Speciality, string Discipline, int DurationInSeconds)
        {
            sName = Name;
            sSpecialityName = Speciality;
            sDiscipline = Discipline;
            CreateDateTime = DateTime.Now;
            nSecondsToTest = Duration;
            File = null;
        }

        public WholeTest(XmlNode WholeTestNode)
        {
            if (WholeTestNode != null)
            {
                try
                {
                    LoadFromXmlNode(WholeTestNode);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось прочитать полный тест из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан xml-узел, из которого необходимо создать полный тест");
        }

        private void ReadFromStream(StreamReader sr)
        {
            XmlDocument Document = new XmlDocument();

            Document.Load(sr);

            XmlNode WholeTest = Document.SelectSingleNode("Test");
            LoadFromXmlNode(WholeTest);
        }

        public Test GenerateTest(int QuestionsNumber, int iTestNumber)
        {
            Test Ret = null;
            int iCurQuestionNum = 0;

            if (QuestionsNumber > 0 && QuestionsNumber < QuestionNumber && iTestNumber > 0)
            {
                try
                {
                    Ret = new Test(iTestNumber, !String.IsNullOrEmpty(sName) ? sName : "_", !String.IsNullOrEmpty(sDiscipline) ? sDiscipline : "_", !String.IsNullOrEmpty(sSpecialityName) ? sSpecialityName : "_", nSecondsToTest);

                    //Random rnd = new Random(DateTime.Now.TimeOfDay.Milliseconds);

                    // Список уже выбранных вопросов
                    List<int> SelectedQuestionNumbers = new List<int>();

                    for (int i = 0; i < QuestionsNumber; i++)
                    {
                        // выберем вопрос из большого теста
                        do
                        {
                            iCurQuestionNum = rnd.Next(Questions.Count);
                        }
                        while(SelectedQuestionNumbers.Contains(iCurQuestionNum));
                        WholeTestQuestion CurWholeQuestion = Questions[iCurQuestionNum];
                        SelectedQuestionNumbers.Add(iCurQuestionNum);

                        // создадим новый вопрос теста-попытки
                        TestQuestion CurQuestion = new TestQuestion(Ret, iCurQuestionNum, i + 1, CurWholeQuestion.Text, CurWholeQuestion.Image, CurWholeQuestion.ThemeName);

                        // возьмем список вариантов ответов вопроса большого теста
                        List<WholeTestQuestionVariant> CurWholeVariants = new List<WholeTestQuestionVariant>();
                        for (int j = 0; j < CurWholeQuestion.VariantNumber; j++)
                            CurWholeVariants.Add(((WholeTestQuestionVariant)((WholeTestQuestion)CurWholeQuestion)[j]));

                        for (int j = 0; j < CurWholeQuestion.VariantNumber; j++)
                        {
                            int iVariant = rnd.Next(CurWholeVariants.Count);
                            CurQuestion.AddVariant(new TestQuestionAnswerVariant(CurQuestion, ((char)('а' + j)), (long)j+1, CurWholeVariants[iVariant].Right, CurWholeVariants[iVariant].Text, CurWholeVariants[iVariant].Image));
                            CurWholeVariants.RemoveAt(iVariant);
                        }

                        Ret.AddQuestion(CurQuestion);
                        //SelectingQuestions.RemoveAt(iCurQuestionNum);
                        //SelectingQuestions.Remove(CurWholeQuestion);
                    }
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось построить тест:" + e1.Message, e1);
                }
            }
            else
                throw new Exception("Неверно указано число вопросов или номер теста");

            return Ret;
        }

        public override int QuestionNumber
        {
            get { return Questions.Count; }
        }

        public override void AddQuestion(CommonQuestion Question)
        {
            if (Question != null)
            {
                Questions.Add((WholeTestQuestion)Question);
            }
            else
                throw new Exception("Попытка добавить пустой вопрос или объект несоответсвующего типа!");
        }

        public override void RemoveQuestion(int QuestionNumber)
        {
            if (QuestionNumber < Questions.Count && QuestionNumber >= 0)
            {
                Questions.RemoveAt(QuestionNumber);
            }
            else
                throw new Exception("Неверно указан номер удаляемого вопроса!");
        }

        public override void RemoveQuestion(CommonQuestion Question)
        {
            if (Question!=null)
            {
                if (Questions.Contains((WholeTestQuestion)Question))
                    Questions.RemoveAt(QuestionNumber);
                else
                    throw new Exception("попытка удалить вопрос, не содержащийся в тесте");
            }
            else
                throw new Exception("Попытка удалить пустой вопрос или объект несоответсвующего типа");
        }

        public override CommonQuestion this[int QuestionIndex]
        {
            get
            {
                if (QuestionIndex >= 0 && QuestionIndex < Questions.Count)
                    return Questions[QuestionIndex];
                else
                    throw new Exception("Поптыка удалить из теста вопрос с номером, которого не существует");
            }
        }

        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlElement WhlTest = Document.CreateElement("Test");
                    XmlAttribute cdt = Document.CreateAttribute("createdate");
                    cdt.Value = Convert.ToString(CreateDateTime);
                    WhlTest.Attributes.Append(cdt);
                    if (!String.IsNullOrEmpty(sSpecialityName))
                    {
                        XmlAttribute spec = Document.CreateAttribute("speciality");
                        spec.Value = sSpecialityName;
                        WhlTest.Attributes.Append(spec);
                    }
                    if (!String.IsNullOrEmpty(sDiscipline))
                    {
                        XmlAttribute dscpln = Document.CreateAttribute("discipline");
                        dscpln.Value = sDiscipline;
                        WhlTest.Attributes.Append(dscpln);
                    }

                    foreach (WholeTestQuestion wtq in Questions)
                    {
                        XmlNode QuestionNode = wtq.ExportToXmlNode(Document);
                        WhlTest.AppendChild(QuestionNode);
                    }

                    return WhlTest;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось сохранить тест в xml-документ: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указан документ, к которому необходимо добавить узел");
        }

        public override void LoadFromXmlNode(XmlNode Node)
        {
            if (Node != null)
            {
                try
                {
                    Questions = new List<WholeTestQuestion>();

                    sName = Node.Attributes["name"].Value;
                    try
                    {
                        sSpecialityName = Node.Attributes["speciality"].Value;
                    }
                    catch
                    {
                        sSpecialityName = "";
                    }
                    try
                    {
                        sDiscipline = Node.Attributes["discipline"].Value;
                    }
                    catch
                    {
                        sDiscipline = "";
                    }
                    try
                    {
                        CreateDateTime = DateTime.Parse(Node.Attributes["createdate"].Value);
                    }
                    catch
                    {
                        CreateDateTime = DateTime.Now;
                    }
                    try
                    {
                        nSecondsToTest = Convert.ToInt32(Node.Attributes["DurationInSeconds"].Value);
                    }
                    catch
                    {
                        nSecondsToTest = -1;
                    }

                    XmlNodeList XmlQuestions = Node.SelectNodes("Question");
                    foreach (XmlNode XmlQuestion in XmlQuestions)
                    {
                        WholeTestQuestion CurQuestion = new WholeTestQuestion(XmlQuestion, this);
                        Questions.Add(CurQuestion);
                    }
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось считать тест из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Попытка загрузить тест из пустого xml-узла");
        }

        public override string ToString()
        {
            return sName + " " + sDiscipline + " " + sSpecialityName;
        }
    }

    /// <summary>
    /// Вопрос полного теста по дисциплине.
    /// </summary>
    public class WholeTestQuestion : CommonQuestion
    {
        protected List<WholeTestQuestionVariant> Variants = null;

        public WholeTestQuestion(XmlNode QuestionNode, WholeTest Test)
        {
            if (QuestionNode != null && Test != null)
            {
                try
                {
                    ParentTest = Test;
                    LoadFromXmlNode(QuestionNode);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось создать тест:" + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не определен xml-узел или тест");
        }

        public WholeTestQuestion(WholeTest Test, string Text, Image Image, string Theme)
        {
            if (Test != null && !String.IsNullOrEmpty(Text))
            {
                try
                {
                    ParentTest = Test;
                    sText = Text;
                    if (Image != null)
                        this.Image = Image;
                    sThemeName = Theme;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось создать тест:" + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не определен тест или текст вопроса");
        }

        public override void AddVariant(CommonAnswerVariant Variant)
        {
            if (Variant != null)
            {
                Variants.Add((WholeTestQuestionVariant)Variant);
            }
            else
                throw new Exception("Попытка добавить пустой вариант ответа");
        }

        public override void RemoveVariant(int VariantNumber)
        {
            if (VariantNumber >= 0 && VariantNumber < Variants.Count)
            {
                Variants.RemoveAt(VariantNumber);
            }
            else
                throw new Exception("Неверно указан номер удаляемого варианта");
        }

        public override void RemoveVariant(CommonAnswerVariant Variant)
        {
            if (Variant != null)
            {
                if(Variants.Contains((WholeTestQuestionVariant)Variant))
                {
                    Variants.Remove((WholeTestQuestionVariant)Variant);
                }
                else
                    throw new Exception("список вариантов не содержит вариант, который вы хотите удалить");
            }
            else
                throw new Exception("Попытка удалить пустой вариант");
        }

        public override int VariantNumber
        {
            get { return Variants.Count; }
        }

        public override CommonAnswerVariant this[int AnswerVariantIndex]
        {
            get 
            {
                if (AnswerVariantIndex >= 0 && AnswerVariantIndex < Variants.Count)
                    return Variants[AnswerVariantIndex];
                else
                    throw new Exception("Попытка обратиться к варианту, не существующему в вопросе");
            }
        }

        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlNode Ret = Document.CreateNode(XmlNodeType.Element, "Question", Document.NamespaceURI);
                    
                    XmlAttribute rgt = Document.CreateAttribute("number");
                    int iQuestionNumber = 0;
                    for (int i = 0; i < ParentTest.QuestionNumber; i++)
                    {
                        if (ParentTest[i] == this)
                        {
                            iQuestionNumber = i;
                            break;
                        }
                    }
                    rgt.Value = Convert.ToString(iQuestionNumber);
                    Ret.Attributes.Append(rgt);
                    
                    XmlAttribute thm = Document.CreateAttribute("theme");
                    thm.Value = ThemeName;
                    Ret.Attributes.Append(thm);

                    XmlElement QText = Document.CreateElement("Text");
                    XmlText QTextTxt = Document.CreateTextNode(sText);
                    QText.AppendChild(QTextTxt);
                    Ret.AppendChild(QText);

                    if (Image != null)
                    {
                        string sImage = TestImage.StringFromImage(Image);
                        XmlNode Img = Document.CreateElement("Image");
                        XmlText ImgTxt = Document.CreateTextNode(sImage);
                        Img.AppendChild(ImgTxt);
                        Ret.AppendChild(Img);
                    }

                    foreach (WholeTestQuestionVariant Vrnt in Variants)
                    {
                        XmlNode VarNode = Vrnt.ExportToXmlNode(Document);
                        Ret.AppendChild(VarNode);
                    }

                    return Ret;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось экспортировать вопрос теста в xml: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указан документ, к которому необходимо добавить узел");
        }

        public override void LoadFromXmlNode(XmlNode Node)
        {
            try
            {
                sThemeName = Node.Attributes["theme"].Value;
            }
            catch
            {
                sThemeName = "";
            }
            sText = Node.SelectSingleNode("Text").InnerText;
            XmlNode ImageNode = Node.SelectSingleNode("Image");
            if (ImageNode != null)
                Image = TestImage.ImageFromString(ImageNode.InnerText);

            Variants = new List<WholeTestQuestionVariant>();
            XmlNodeList VariantNodes = Node.SelectNodes("Variant");
            foreach (XmlNode VariantNode in VariantNodes)
            {
                WholeTestQuestionVariant CurVariant = new WholeTestQuestionVariant(VariantNode, this);
                Variants.Add(CurVariant);
            }
        }
    }

    /// <summary>
    /// Вариант ответа на полный тест по дисциплине.
    /// </summary>
    public class WholeTestQuestionVariant:CommonAnswerVariant
    {
        public WholeTestQuestionVariant(XmlNode VariantNode, WholeTestQuestion Question)
        {
            if (VariantNode != null && Question != null)
            {
                ParentQuestion = Question;
                LoadFromXmlNode(VariantNode);
            }
            else
                throw new Exception("Не задан xml-узел или вопрос");
        }

        public WholeTestQuestionVariant(string VariantText, bool RightVariant, Image Image, WholeTestQuestion Question)
        {
            if (!String.IsNullOrEmpty(VariantText) && Question!=null)
            {
                try
                {
                    ParentQuestion = Question;
                    sText = VariantText;
                    blRight = RightVariant;
                    if (Image != null)
                        this.Image = Image;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось создать вариант ответа на вопрос:" + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан текст варианта или не указан базовый вопрос");
        }

        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlNode Ret = Document.CreateElement("Variant");
                    XmlAttribute rgt = Document.CreateAttribute("right");
                    rgt.Value = blRight ? "+" : "-";
                    Ret.Attributes.Append(rgt);
                    XmlElement Txt = Document.CreateElement("Text");
                    XmlText TextTxt = Document.CreateTextNode(sText);
                    Txt.AppendChild(TextTxt);
                    Ret.AppendChild(Txt);

                    if (Image != null)
                    {
                        string sImage = TestImage.StringFromImage(Image);
                        XmlNode Img = Document.CreateElement("Image");
                        XmlText ImgTxt = Document.CreateTextNode(sImage);
                        Img.AppendChild(ImgTxt);
                        Ret.AppendChild(Img);
                    }

                    return Ret;
                }
                catch
                {
                    throw new Exception("Не удалось экспортировать вариант ответа в xml");
                }
            }
            else
                throw new Exception("Не указан документ, к которому необходимо добавить узел");
        }

        public override void LoadFromXmlNode(XmlNode Node)
        {
            try
            {
                XmlNode TextNode = Node.SelectSingleNode("Text");
                if (TextNode != null)
                    sText = TextNode.InnerText;
                blRight = Node.Attributes["right"].Value == "+" ? true : false;
                XmlNode ImageNode = Node.SelectSingleNode("Image");
                if (ImageNode != null)
                    Image = TestImage.ImageFromString(ImageNode.InnerText);
            }
            catch (Exception e1)
            {
                throw new Exception("Не удалось создать вариант ответа на вопрос:" + e1.Message, e1);
            }
        }
    }

    /// <summary>
    /// Тест для отдельной попытки студента, включает
    /// вопросы из WholeTest с указанием их номеров и порядковых номеров,
    /// варианты ответов обозначены буквами.
    /// Можно сохранять в xml-файл.
    /// При сохранении включает только вопросы этого теста.
    /// </summary>
    public class Test:CommonTest
    {
        protected long iNumber = -1;
        protected double flUpperBorder = -1;

        protected List<TestQuestion> Questions = null;

        public long TestNumber
        {
            get { return iNumber; }
        }
        public double UpperBorder
        {
            get 
            {
                if (flUpperBorder == -1)
                    CalculateUpperBorder();

                return flUpperBorder; 
            }
        }

        public override void AddQuestion(CommonQuestion Question)
        {
            if (Questions != null && Question.Test==this)
            {
                Questions.Add((TestQuestion)Question);
                flUpperBorder = -1;
            }
            else
                throw new Exception("Попытка добавить несуществующий вопрос, или вопрос не из этого теста");
        }
        
        public override void RemoveQuestion(int iQuestion)
        {
            if (iQuestion >= 0 && iQuestion < Questions.Count)
            {
                Questions.RemoveAt(iQuestion);
                flUpperBorder = -1;
            }
            else
                throw new Exception("Неверно указан номер вопроса");
        }
        
        public override void RemoveQuestion(CommonQuestion Question)
        {
            if (Question != null && Questions.Contains((TestQuestion)Question))
            {
                Questions.Remove((TestQuestion)Question);
                flUpperBorder = -1;
            }
            else
                throw new Exception("Не определен вопрос, который необходимо удалить, либо удаляемый вопрос не содержится в списке вопросов");
        }
        
        public override int QuestionNumber
        {
            get { return Questions.Count; }
        }
        
        public long VariantsInQuestion(int iOrderQuestionNum)
        {
            long iRet = -1;

            if (iOrderQuestionNum > 0 && iOrderQuestionNum <= Questions.Count)
                iRet = Questions[iOrderQuestionNum - 1].VariantsNumber;

            return iRet;
        }

        public bool LoadFromStream(StreamReader Reader)
        {
            bool blRet = false;

            iNumber = -1;
            flUpperBorder = -1;

            try
            {
                XmlDocument TestXml = new XmlDocument(); ;

                TestXml.Load(Reader);
                XmlNode WholeTest = TestXml.DocumentElement;

                LoadFromXmlNode(WholeTest);

                blRet = true;
            }
            catch (Exception e1)
            {
                throw e1;
            }

            return blRet;
        }

        public Test(string sFileName)
        {
            if (System.IO.File.Exists(sFileName))
            {
                File = new FileInfo(sFileName);
                
                StreamReader sr = new StreamReader(sFileName);
                LoadFromStream(sr);
            }
        }

        public Test(StreamReader sr)
        {
            LoadFromStream(sr);
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="TestNumber"></param>
        /// <param name="Name"></param>
        /// <param name="Discipline"></param>
        /// <param name="Speciality"></param>
        /// <param name="DurationInSeconds">Продолжительность теста в секундах, -1 - не ограничена</param>
        public Test(int TestNumber, string Name, string Discipline, string Speciality, int DurationInSeconds)
        {
            if (TestNumber > 0 && !String.IsNullOrEmpty(Name) && !String.IsNullOrEmpty(Discipline) && !String.IsNullOrEmpty(Speciality) && (DurationInSeconds>0 || DurationInSeconds==-1))
            {
                iNumber = TestNumber;
                flUpperBorder = -1;
                sName = Name;
                sDiscipline = Discipline;
                sSpecialityName = Speciality;
                nSecondsToTest = DurationInSeconds;
                try
                {
                    Questions = new List<TestQuestion>();
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось создать набор ответов в тесте: " + e1.Message);
                }
            }
            else
            {
                throw new Exception("Не удалось создать тест: Неверно задан номер теста, его назание или названия дисциплины или специальности, или продолжительность теста");
            }
        }

        public Test(XmlNode TestNode)
        {
            if (TestNode != null)
            {
                try
                {
                    LoadFromXmlNode(TestNode);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось загрузить тест из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан xml-узел, из которого необходимо создать тест");
        }
        
        protected void CalculateUpperBorder()
        {
            const int nTries = 8000;
//            SortedDictionary<double, int> Distribution = new SortedDictionary<double, int>();
            SortedDictionary<double, int> newDistribution = new SortedDictionary<double, int>();
            SortedDictionary<double, int> lastDistribution = new SortedDictionary<double, int>();

            Group FakeGroup = new Group("Fakegroup", "Fakespeciality", 1991);
            Student FakeStudent = new Student("fake", "fake", "fake", FakeGroup); ;
            StudentTestAnswer NewFakeAnswer = null;

//            for (int i = 0; i < nTries; i++)
//            {
//                NewFakeAnswer = GenerateRandomAnswer(FakeStudent);
//
//                double flBall = CalculateResult(NewFakeAnswer);
//                if (Distribution.ContainsKey(flBall))
//                    Distribution[flBall]++;
//                else
//                    Distribution.Add(flBall, 1);
//           }

            for (int i = 0; i < 40000; i++)
            {
                NewFakeAnswer = GenerateRandomAnswer(FakeStudent);

                double flBall = CalculateResult(NewFakeAnswer);
                if (newDistribution.ContainsKey(flBall))
                    newDistribution[flBall]++;
                else
                    newDistribution.Add(flBall, 1);
            }

            //do
            //{
            //    NewFakeAnswer = GenerateRandomAnswer(FakeStudent);
            //    lastDistribution = new SortedDictionary<double,int>(newDistribution);

            //    double flBall = CalculateResult(NewFakeAnswer);
            //    if (newDistribution.ContainsKey(flBall))
            //        newDistribution[flBall]++;
            //    else
            //        newDistribution.Add(flBall, 1);
            //} while(newDistribution.Count > lastDistribution.Count || compareDistributions(lastDistribution, newDistribution) > precision) ;

            List<double> Keys = new List<double>();
            Keys.AddRange(newDistribution.Keys);
            Keys.Sort();
            flUpperBorder = Keys[Keys.Count - 1];

            string keys = "";
            string results = "";
            foreach (KeyValuePair<double, int> curPair in newDistribution)
            {
                keys += (String.Format("{0:##.00}", curPair.Key * 100) + "\r\n");
                results += (curPair.Value.ToString() + "\r\n");
            }

            for (int i = Keys.Count - 1; i >= 0; i--)
            {
                double flFreq = ((double)newDistribution[Keys[i]] / (double)nTries);
                if (flFreq > 0.05)
                {
                    flUpperBorder = Keys[i];
                    break;
                }
            }
        }

        private double compareDistributions(SortedDictionary<double, int> lastDistribution, SortedDictionary<double, int> newDistribution)
        {
            double ret = 0;

            if (lastDistribution.Count == newDistribution.Count)
            {
                List<double> keys = new List<double>();
                double sum = 0;

                foreach (double curKey in lastDistribution.Keys)
                    if (!keys.Contains(curKey)) {
                        keys.Add(curKey);
                        sum += lastDistribution[curKey];
                    }
                foreach (double curKey in newDistribution.Keys)
                    if (!keys.Contains(curKey)) {
                        keys.Add(curKey);
                        sum += newDistribution[curKey];
                    }

                foreach (double curKey in keys)
                    ret += Math.Pow(newDistribution[curKey] / sum - lastDistribution[curKey] / sum, 2);

                ret = Math.Sqrt(ret);
            }
            else
                ret = double.MaxValue;

            return ret;
        }


        /// <summary>
        /// Определяет, принадлежат ли результаты тестирования к одной и той же генеральной совокупности
        /// </summary>
        /// <param name="FirstPicks"></param>
        /// <param name="SecondPicks"></param>
        /// <returns></returns>
        public bool IsSamePicks(ICollection<StudentTestAnswer> FirstPicks, ICollection<StudentTestAnswer> SecondPicks)
        {
            bool blRet = false;

            if (FirstPicks != null && SecondPicks != null)
            {
                if (FirstPicks.Count >= 3 && SecondPicks.Count >= 3)
                {
                    List<StudentTestAnswer> WholeTries = new List<StudentTestAnswer>();
                    WholeTries.AddRange(FirstPicks);
                    WholeTries.AddRange(SecondPicks);

                    WholeTries.Sort(TriesComparerByPercent);

                    int n1 = 0, n2 = 0;
                    for (int i = 0; i < WholeTries.Count; i++)
                        if (FirstPicks.Contains(WholeTries[i]))
                            n1 += (i + 1);
                        else
                            n2 += (i + 1);

                    int nx=FirstPicks.Count;
                    int iTx = n1;
                    if (n2 > n1)
                    {
                        nx = SecondPicks.Count;
                        iTx = n2;
                    }

                    int iU = FirstPicks.Count * SecondPicks.Count + (nx * (nx + 1)) / 2 - iTx;
                }
                else
                    throw new Exception("Не выполняются условия количества тестов выборке");
            }
            else
                throw new Exception("Попытка сравнить выборки, как минимум одна из которых пуста");

            return blRet;
        }

        private int TriesComparerByPercent(StudentTestAnswer Test1, StudentTestAnswer Test2)
        {
            int iRet = -1;

            if (Test1.PassedTest.CalculateResult(Test1) == Test2.PassedTest.CalculateResult(Test2))
                iRet = 0;
            else if (Test1.PassedTest.CalculateResult(Test1) > Test2.PassedTest.CalculateResult(Test2))
                iRet = 1;

            return iRet;
        }
        
        
        /// <summary>
        /// Генерирует случайный ответ для заданного студента
        /// </summary>
        /// <param name="FakeStudent"></param>
        /// <returns></returns>
        public StudentTestAnswer GenerateRandomAnswer(Student FakeStudent)
        {
            StudentTestAnswer NewFakeAnswer = null;

            NewFakeAnswer = new StudentTestAnswer(this, FakeStudent, DateTime.Now);
            for (int j = 0; j < Questions.Count; j++)
                if (Questions[j].RightVariantsNumber == 1)
                {
                    char cVariantLetter = ((char)('а' + rnd.Next(((int)Questions[j].VariantsNumber) - 1)));
                    NewFakeAnswer.AnswerQuestion(Questions[j].OrderQuestionNumber, cVariantLetter);
                }
                else
                {
                    //список возможных вариантов ответа
                    List<char> cVariants = new List<char>();
                    for (char cLetter = 'а'; cLetter < ('а' + ((int)Questions[j].VariantsNumber)); cLetter++)
                        cVariants.Add(cLetter);

                    // случайное число ответов
                    int nAnswerdVariants = rnd.Next(((int)Questions[j].VariantsNumber) - 1) + 1;
                    for (int k = 0; k < nAnswerdVariants; k++)
                    {
                        int iVariantNum = rnd.Next(cVariants.Count);
                        char cVariantLetter = cVariants[iVariantNum];
                        cVariants.Remove(cVariantLetter);
                        NewFakeAnswer.AnswerQuestion(Questions[j].OrderQuestionNumber, cVariantLetter);
                    }
                }

            return NewFakeAnswer;
        }

        /// <summary>
        /// Добавляет к словарю ошибок ошибки, допущенные в данном ответе
        /// </summary>
        /// <param name="Answer">Анализируемый ответ</param>
        /// <param name="ErrorDict">Словарь ошибок</param>
        public void AnswerErrors(StudentTestAnswer Answer, Dictionary<string, int> ErrorDict)
        {
            if (Answer != null && ErrorDict != null)
            {
                foreach (TestQuestion CurQuestion in Questions)
                {
                    for (int i = 0; i < CurQuestion.VariantsNumber; i++)
                    {
                        if (CurQuestion.RightVariant(i))
                        {
                            if (!Answer.AnsweredVariant(CurQuestion.OrderQuestionNumber, ((char)('а' + i))))
                                AddErrorThemeNameToDict(ErrorDict, CurQuestion);
                        }
                        else
                        {
                            if (Answer.AnsweredVariant(CurQuestion.OrderQuestionNumber, ((char)('а' + i))))
                                AddErrorThemeNameToDict(ErrorDict, CurQuestion);
                        }
                    }
                }
            }
            else
                throw new Exception("Не определен ответ на вопросы теста, или не определен словарь ошибок");
        }

        private void AddErrorThemeNameToDict(Dictionary<string, int> ErrorDict, TestQuestion CurQuestion)
        {
            try
            {
                if (!ErrorDict.ContainsKey(CurQuestion.ThemeName))
                    ErrorDict.Add(CurQuestion.ThemeName, 1);
                else
                    ErrorDict[CurQuestion.ThemeName]++;
            }
            catch(Exception e1)
            {
                throw new Exception("Не удалось добавить имя темы: "+e1.Message, e1);
            }
        }
        
        /// <summary>
        /// Результат теста
        /// </summary>
        /// <param name="Answer"></param>
        /// <returns></returns>
        public double CalculateResult(StudentTestAnswer Answer)
        {
            if (Answer != null)
            {
                try
                {
                    double flRet = -1;
                    long nRightVariantsInTest = 0;
                    long nNotRightVariantsInTest = 0;
                    long nAnsweredRightVariants = 0;
                    long nNotAnsweredNotRightVariants = 0;
                    double flRightAnswersResult = 0;
                    double flNotRightAnswersResult = 0;

                    foreach (TestQuestion CurQuestion in Questions)
                    {
                        nRightVariantsInTest += CurQuestion.RightVariantsNumber;
                        nNotRightVariantsInTest += (CurQuestion.VariantsNumber - CurQuestion.RightVariantsNumber);

                        for (int i = 0; i < CurQuestion.VariantsNumber; i++)
                        {
                            if (CurQuestion.RightVariant(i))
                            {
                                if (Answer.AnsweredVariant(CurQuestion.OrderQuestionNumber, ((char)('а' + i))))
                                    nAnsweredRightVariants++;
                            }
                            else
                            {
                                if (!Answer.AnsweredVariant(CurQuestion.OrderQuestionNumber, ((char)('а' + i))))
                                    nNotAnsweredNotRightVariants++;
                            }
                        }
                    }

                    if (nRightVariantsInTest == 0)
                        nRightVariantsInTest++;
                    if (nNotRightVariantsInTest == 0)
                        nNotRightVariantsInTest++;

                    flRightAnswersResult = (double)nAnsweredRightVariants / (double)nRightVariantsInTest;
                    flNotRightAnswersResult = (double)nNotAnsweredNotRightVariants / (double)nNotRightVariantsInTest;

                    flRet = flRightAnswersResult <= flNotRightAnswersResult ? flRightAnswersResult : flNotRightAnswersResult;

                    return flRet;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось посчитать результат прохождения теста: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан ответ, для которого необходимо подсчитать результат");
        }

        public double RecievedBall(StudentTestAnswer Answer)
        {
            if (Answer != null)
            {
                try
                {
                    if (flUpperBorder == -1)
                        CalculateUpperBorder();

                    double flRet = 0;
                    double flResult = CalculateResult(Answer);
                    flRet = (flResult - flUpperBorder) * (1.0 / (1.0 - flUpperBorder));

                    return flRet >= 0 ? flRet : 0;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось подсчитать плоченный балл: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан ответ, для которого необходимо подсчитать результат");
        }

        public override CommonQuestion this[int QuestionIndex]
        {
            get 
            {
                if (QuestionIndex >= 0 && QuestionIndex < Questions.Count)
                    return Questions[QuestionIndex];
                else
                    throw new Exception("Попытка обратиться к вопросу, которого нет в тесте");
            }
        }

        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlElement TestNode = Document.CreateElement("Test");
                    XmlAttribute TestNum = Document.CreateAttribute("number");
                    TestNum.Value = Convert.ToString(iNumber);
                    TestNode.Attributes.Append(TestNum);

                    XmlAttribute TestBorder = Document.CreateAttribute("UpperBorder");
                    TestBorder.Value = Convert.ToString(flUpperBorder);
                    TestNode.Attributes.Append(TestBorder);

                    foreach (TestQuestion tq in Questions)
                        TestNode.AppendChild(tq.ExportToXmlNode(Document));

                    return TestNode;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось сохранить тест в xml-узел: "+e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указан документ, к которому необходимо добавить тест");
        }

        public override void LoadFromXmlNode(XmlNode Node)
        {
            if (Node != null)
            {
                try
                {
                    iNumber = Convert.ToInt64(Node.Attributes["number"].Value);
                    try
                    {
                        sName = Node.Attributes["name"].Value;
                    }
                    catch
                    {
                        sName = "";
                    }
                    try
                    {
                        sDiscipline = Node.Attributes["discipline"].Value;
                    }
                    catch
                    {
                        sDiscipline = "";
                    }
                    try
                    {
                        sSpecialityName = Node.Attributes["speciality"].Value;
                    }
                    catch
                    {
                        sSpecialityName = "";
                    }
                    try
                    {
                        nSecondsToTest = Convert.ToInt32(Node.Attributes["DurationInSeconds"].Value);
                    }
                    catch
                    {
                        nSecondsToTest = -1;
                    }

                    XmlNodeList Nodes = Node.ChildNodes;

                    Questions = new List<TestQuestion>();

                    foreach (XmlNode CurQuestion in Nodes)
                    {
                        TestQuestion NewQuestion = new TestQuestion(this, Convert.ToInt64(CurQuestion.Attributes["testnumber"].Value), Convert.ToInt64(CurQuestion.Attributes["ordernumber"].Value), CurQuestion);
                        Questions.Add(NewQuestion);
                    }

                    flUpperBorder = -1;
                    //CalculateUpperBorder();
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось прочитать тест из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан узел, из которого будет прочитан тест");
        }

        public override string ToString()
        {
            return Convert.ToString(iNumber) + " " + base.ToString();
        }
    }

    /// <summary>
    /// Вопрос теста-попытки (Test).
    /// </summary>
    public class TestQuestion:CommonQuestion
    {
        protected long iTestQuestionNumber;
        protected long iOrderQuestionNumber;

        protected List<TestQuestionAnswerVariant> Variants;

        public long TestQuestionNumber
        {
            get { return iTestQuestionNumber; }
        }
        public long OrderQuestionNumber
        {
            get { return iOrderQuestionNumber; }
        }
        public long VariantsNumber
        {
            get { return Variants.Count; }
        }
        public long RightVariantsNumber
        {
            get
            {
                long nVars = 0;
                for (int i = 0; i < Variants.Count; i++)
                    if (Variants[i].Right)
                        nVars++;

                return nVars;
            }
        }

        public TestQuestion(Test Test, long TestQuestionNumber, long OrderQuestionNumber, string Text, Image Image, string sThemeName)
        {
            if (Test!=null && TestQuestionNumber >= 0 && OrderQuestionNumber > 0 && !String.IsNullOrEmpty(Text))
            {
                try
                {
                    ParentTest = Test;
                    iTestQuestionNumber = TestQuestionNumber;
                    iOrderQuestionNumber = OrderQuestionNumber;
                    Variants = new List<TestQuestionAnswerVariant>();
                    sText = Text;
                    this.sThemeName = sThemeName;

                    if (Image != null)
                        this.Image = Image;
                }
                catch (Exception e1)
                {
                    throw new Exception("Невозможно создать новый вопрос: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Неверно указан номер создаваемого вопроса или не задан текст вопроса");
        }

        public TestQuestion(Test Test, long TestQuestionNumber, long OrderQuestionNumber, string Text, Image QuestionImage, XmlNodeList VariantNodes)
        {
            if (Test!=null && TestQuestionNumber >= 0 && OrderQuestionNumber > 0 && !String.IsNullOrEmpty(Text) && VariantNodes != null)
            {
                try
                {
                    ParentTest = Test;
                    iTestQuestionNumber = TestQuestionNumber;
                    iOrderQuestionNumber = OrderQuestionNumber;
                    Variants = new List<TestQuestionAnswerVariant>();
                    sText = Text;
                    if (QuestionImage != null)
                        this.QuestionImage = QuestionImage;

                    for (int i = 0; i < VariantNodes.Count; i++)
                    {
                        XmlNode CurVariantNode = VariantNodes[i];

                        XmlNode ImageNode=CurVariantNode.SelectSingleNode("Image");
                        System.Drawing.Image VariantImage=null;
                        if(ImageNode!=null)
                            VariantImage=TestImage.ImageFromXmlNode(ImageNode, Test);

                        string sVariantText = CurVariantNode.SelectSingleNode("Text").InnerText;
                        TestQuestionAnswerVariant NewVariant = new TestQuestionAnswerVariant(this, Convert.ToChar(CurVariantNode.Attributes["letter"].Value), i + 1, Convert.ToString(CurVariantNode.Attributes["right"].Value) == "+", sVariantText, VariantImage);
                        Variants.Add(NewVariant);
                    }
                }
                catch (Exception e1)
                {
                    throw new Exception("невозможно создать вопрос: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Неправильный номер вопроса, или не задан номер вопроса, или не указаны узлы вариантов ответов");
        }

        public TestQuestion(Test Test, long TestQuestionNumber, long OrderQuestionNumber, XmlNode QuestionNode)
        {
            if (Test!=null && TestQuestionNumber >= 0 && OrderQuestionNumber > 0 && QuestionNode!=null)
            {
                try
                {
                    ParentTest = Test;
                    iTestQuestionNumber = TestQuestionNumber;
                    iOrderQuestionNumber = OrderQuestionNumber;

                    XmlNode QText = QuestionNode.SelectSingleNode("Text");
                    sText = QText.InnerText;

                    try
                    {
                        sThemeName = QuestionNode.Attributes["ThemeName"].Value;
                    }
                    catch
                    {
                    }

                    XmlNode QImage = QuestionNode.SelectSingleNode("Image");
                    if(QImage!=null)
                        Image = TestImage.ImageFromXmlNode(QImage, ParentTest);

                    XmlNodeList VariantNodes = QuestionNode.SelectNodes("Variant");

                    Variants = new List<TestQuestionAnswerVariant>();
                    for (int i = 0; i < VariantNodes.Count; i++)
                    {
                        XmlNode CurVariantNode = VariantNodes[i];

                        //XmlNode ImageNode = CurVariantNode.SelectSingleNode("Image");
                        //System.Drawing.Image VariantImage = null;
                        //if (ImageNode != null)
                        //    VariantImage = TestImage.ImageFromXmlNode(ImageNode, Test);

                        //string sVariantText = CurVariantNode.SelectSingleNode("Text").InnerText;

                        //TestQuestionAnswerVariant NewVariant = new TestQuestionAnswerVariant(this, Convert.ToChar(CurVariantNode.Attributes["letter"].Value), i + 1, Convert.ToString(CurVariantNode.Attributes["right"].Value) == "+", sVariantText, VariantImage);
                        TestQuestionAnswerVariant NewVariant = new TestQuestionAnswerVariant(this, CurVariantNode);
                        Variants.Add(NewVariant);
                    }
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось прочитать вопрос из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Неправильный номер вопроса, или не задан номер вопроса, или не указаны узлы вариантов ответов");
        }

        public TestQuestion(Test Test, XmlNode TestQuestionNode)
        {
            if (TestQuestionNode != null && Test!=null)
            {
                try
                {
                    LoadFromXmlNode(TestQuestionNode);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось загрузить вопрос теста из xml-узла: "+e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан xml-узел, из которого создается вопрос теста");
        }
        
        public bool RightVariant(char cVarinatName)
        {
            bool blRet = false;

            for (int i = 0; i < Variants.Count; i++)
                if (Variants[i].VariantName == cVarinatName)
                {
                    blRet = Variants[i].Right;
                    break;
                }

            return blRet;
        }

        public bool RightVariant(int iVariantNumber)
        {
            if (iVariantNumber >= 0 && iVariantNumber < Variants.Count)
                return Variants[iVariantNumber].Right;
            else
                throw new Exception("Номер варианта не соответствует количеству вариантов, существующих в вопросе");
        }

        public override int VariantNumber
        {
            get { return Variants.Count; }
        }

        public override void AddVariant(CommonAnswerVariant Variant)
        {
            if (Variant != null)
                Variants.Add((TestQuestionAnswerVariant)Variant);
            else
                throw new Exception("Не задан вариант, который надо добавить");
        }

        public override void RemoveVariant(int VariantNumber)
        {
            if (VariantNumber >= 0 && VariantNumber < Variants.Count)
                Variants.RemoveAt(VariantNumber);
            else
                throw new Exception("Номер варианта за границами допустимого числа вариантов");
        }

        public override void RemoveVariant(CommonAnswerVariant Variant)
        {
            if (Variant != null)
            {
                if (Variants.Contains((TestQuestionAnswerVariant)Variant))
                    Variants.Remove((TestQuestionAnswerVariant)Variant);
                else
                    throw new Exception("Попытка удалить вариант, не существующий в данном вопросе");
            }
            else
                throw new Exception("Попытка удалить пустой вариант");
        }

        public override CommonAnswerVariant this[int AnswerVariantIndex]
        {
            get
            {
                if (AnswerVariantIndex >= 0 && AnswerVariantIndex < Variants.Count)
                    return Variants[AnswerVariantIndex];
                else
                    throw new Exception("Попытка обратиться к варианту, которого нет в вопросе");
            }
        }

        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlElement QNode = Document.CreateElement("Question");
                    XmlAttribute TNum = Document.CreateAttribute("testnumber");
                    TNum.Value = Convert.ToString(iTestQuestionNumber);
                    QNode.Attributes.Append(TNum);

                    XmlAttribute OQNum = Document.CreateAttribute("ordernumber");
                    OQNum.Value = Convert.ToString(iOrderQuestionNumber);
                    QNode.Attributes.Append(OQNum);

                    if(!String.IsNullOrEmpty(sThemeName))
                    {
                        XmlAttribute QThemeAttr = Document.CreateAttribute("ThemeName");
                        QThemeAttr.Value = sThemeName;
                        QNode.Attributes.Append(QThemeAttr);
                    }

                    XmlElement QText = Document.CreateElement("Text");
                    XmlText QTextTxt = Document.CreateTextNode(sText);
                    QText.AppendChild(QTextTxt);
                    QNode.AppendChild(QText);

                    if (Image != null)
                    {
                        string sImage = TestImage.StringFromImage(Image);
                        XmlElement Img = Document.CreateElement("Image");
                        XmlText ImgTxt = Document.CreateTextNode(sImage);
                        Img.AppendChild(ImgTxt);
                        QNode.AppendChild(Img);
                    }

                    foreach (TestQuestionAnswerVariant tqav in Variants)
                        QNode.AppendChild(tqav.ExportToXmlNode(Document));

                    return QNode;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось сохранить вопрос в xml-узел: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указан документ, к которому добавляется узел вопроса теста");
        }

        public override void LoadFromXmlNode(XmlNode Node)
        {
            throw new NotImplementedException();
        }
    }

    /// <summary>
    /// Вариант ответа на вопрос теста-попытки.
    /// </summary>
    public class TestQuestionAnswerVariant:CommonAnswerVariant
    {
        protected long iOrderNumber;
        protected char cVariantName;

        /// <summary>
        /// Порядковый номер варианта ответа в вопросе.
        /// </summary>
        public long OrderNumber
        {
            get { return iOrderNumber; }
        }
        /// <summary>
        /// Буква варианта в ответе.
        /// </summary>
        public char VariantName
        {
            get { return cVariantName; }
        }

        public TestQuestionAnswerVariant(TestQuestion Parent, char cName, long OrderNumber, bool Right, string Text, Image Image)
        {
            if (Parent != null && cName != '\0' && cName >= 'а' && cName <= 'я' && OrderNumber > 0 && Text != null)
            {
                ParentQuestion = Parent;
                iOrderNumber = OrderNumber;
                blRight = Right;
                cVariantName = cName;
                sText = Text;
                if (Image != null)
                    this.Image = Image;
            }
            else
                throw new Exception("Ошибочные данные");
        }

        public TestQuestionAnswerVariant(TestQuestion Parent, XmlNode TestQuestionAnswerVariantNode)
        {
            if (Parent != null && TestQuestionAnswerVariantNode!=null)
            {
                ParentQuestion = Parent;
                try
                {
                    LoadFromXmlNode(TestQuestionAnswerVariantNode);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось загрузить вариант ответа из xml-узла: "+e1.Message, e1);
                }
            }
            else
                throw new Exception("Не указан вопрос, к которому относится вариант, или не задан xml-узел варианта");
        }

        public override string ToString()
        {
            return String.Format("{0} {1} {2}", cVariantName, blRight ? "+" : "-", sText);
        }

        /// <summary>
        /// Экспортирует вариант ответа в xml-узел
        /// </summary>
        /// <param name="Document"></param>
        /// <returns></returns>
        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlElement ANode = Document.CreateElement("Variant");
                    XmlAttribute lett = Document.CreateAttribute("letter");
                    lett.Value = Convert.ToString(cVariantName);
                    ANode.Attributes.Append(lett);
                    XmlAttribute rgt = Document.CreateAttribute("right");
                    rgt.Value = blRight ? "+" : "-";
                    ANode.Attributes.Append(rgt);

                    XmlElement AText = Document.CreateElement("Text");
                    XmlText ATextTxt = Document.CreateTextNode(sText);
                    AText.AppendChild(ATextTxt);
                    ANode.AppendChild(AText);

                    if (Image != null)
                    {
                        string sImage = TestImage.StringFromImage(Image);
                        XmlElement Img = Document.CreateElement("Image");
                        XmlText ImgTxt = Document.CreateTextNode(sImage);
                        Img.AppendChild(ImgTxt);
                        ANode.AppendChild(Img);
                    }

                    return ANode;
                }
                catch (Exception e1)
                {
                    throw new Exception("не удалось экспортировать вариант ответа в xml-узел: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан документ, для которого создается узел вопроса");
        }

        /// <summary>
        /// Загружает вариант ответа из xml-узла.
        /// </summary>
        /// <param name="Node"></param>
        public override void LoadFromXmlNode(XmlNode Node)
        {
            if (Node != null)
            {
                try
                {
                    blRight = Node.Attributes["right"].Value == "+";
                    sText = Node.SelectSingleNode("Text").InnerText;
                    cVariantName = Node.Attributes["letter"].Value[0];
                    XmlNode ImageNode = Node.SelectSingleNode("Image");
                    System.Drawing.Image VariantImage = null;
                    if (ImageNode != null)
                        VariantImage = TestImage.ImageFromXmlNode(ImageNode, null);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось прочитать тест из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан узел, из которого будет прочитан вариант ответа");
        }
    }

    /// <summary>
    /// Ответ студента на тест-попытку. 
    /// Можно сохранять в xml-файл.
    /// При сохранении в xml включает информацию о студенте (и его группе)
    /// и сам тест, на который отвечает студент.
    /// </summary>
    public class StudentTestAnswer:BaseObject
    {
        protected Student Student = null;

        protected Test Test = null;
        protected Dictionary<long, TestQuestionAnswer> StudentAnswers = null;
        protected DateTime ExecutionDateTime;
        protected int iCurrentQuestion = 0;
        protected int nSecondsFromStart = 0;

        private enum Direction
        {
            Forward,
            Backward
        }

        /// <summary>
        /// Студент, который проходит тест
        /// </summary>
        public Student PassingStudent
        {
            get { return Student; }
        }
        /// <summary>
        /// Проходимый тест
        /// </summary>
        public Test PassedTest
        {
            get { return Test; }
        }

        public int CurrentQuestionNumber
        {
            get { return iCurrentQuestion; }
        }

        public void MoveNext(int SecondsFromPreviousAnswer)
        {
            Move(Direction.Forward, SecondsFromPreviousAnswer);
        }

        public void MovePrev(int SecondsFromPreviousAnswer)
        {
            Move(Direction.Backward, SecondsFromPreviousAnswer);
        }

        private void Move(Direction Dir, int SecondsFromPreviousAnswer)
        {
            if (Dir == Direction.Forward)
            {
                if (SecondsFromPreviousAnswer > 0)
                {
                    if (iCurrentQuestion < (Test.QuestionNumber - 1))
                        iCurrentQuestion++;
                }
                else
                    throw new Exception("Неверно задано число секунд, прошедшее с предыдущего ответа");
            }
            else
            {
                if (SecondsFromPreviousAnswer > 0)
                {
                    if (iCurrentQuestion > 0)
                        iCurrentQuestion--;
                }
                else
                    throw new Exception("Неверно задано число секунд, прошедшее с предыдущего ответа");
            }

            nSecondsFromStart += SecondsFromPreviousAnswer;
            if (nSecondsFromStart > Test.Duration && Test.Duration > 0)
                throw new TimesUpException();
        }

        public void MoveToQuestion(int QuestionNum, int SecondsFromPreviousAnswer)
        {
            if (SecondsFromPreviousAnswer > 0)
            {
                if (QuestionNum >= 0 && QuestionNum < Test.QuestionNumber)
                    iCurrentQuestion = QuestionNum;
                else
                    throw new Exception("Попытка перейти к вопросу, который отсутствует в тесте");
            }
            else
                throw new Exception("Неверно задано число секунд, прошедшее с предыдущего ответа");

            nSecondsFromStart += SecondsFromPreviousAnswer;
            if (nSecondsFromStart > Test.Duration && Test.Duration > 0)
                throw new TimesUpException();
        }

        /// <summary>
        /// Создает новыый пустой набор ответов студента на тест.
        /// </summary>
        /// <param name="PassingTest"></param>
        /// <param name="PassingStudent"></param>
        /// <param name="ExecutionDateTime"></param>
        public StudentTestAnswer(Test PassingTest, Student PassingStudent, DateTime ExecutionDateTime)
        {
            if (PassingTest != null && PassingStudent != null)
            {
                try
                {
                    Test = PassingTest;
                    Student = PassingStudent;
                    this.ExecutionDateTime = ExecutionDateTime;

                    StudentAnswers = new Dictionary<long, TestQuestionAnswer>();
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось создать ответы студента на тест: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан тест или студент, проходящий тест");
        }

        /// <summary>
        /// Создает новыый набор ответов студента на тест из xml-узла.
        /// </summary>
        /// <param name="PassingTest">Тест</param>
        /// <param name="PassingStudent">Студент</param>
        /// <param name="StudentTestAnswerNode">xml-узел (в нем - только ответы!)</param>
        public StudentTestAnswer(Test PassingTest, Student PassingStudent, XmlNode StudentTestAnswerNode)
        {
            if (PassingTest != null && PassingStudent != null && StudentTestAnswerNode!=null)
            {
                try
                {
                    Test = PassingTest;
                    Student = PassingStudent;
                    this.ExecutionDateTime = Convert.ToDateTime(StudentTestAnswerNode.Attributes["executiondatetime"].Value);

                    StudentAnswers = new Dictionary<long, TestQuestionAnswer>();
                    LoadFromXmlNode(StudentTestAnswerNode);
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось создать ответы студента на тест: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан тест или студент, проходящий тест");
        }

        /// <summary>
        /// Создает ответ из xml-потока. В потоке - ответы, сам тест, информация о студенте и его группе.
        /// </summary>
        /// <param name="XmlStream"></param>
        public StudentTestAnswer(Stream XmlStream)
        {
            if (XmlStream != null)
            {
                StudentAnswers = new Dictionary<long, TestQuestionAnswer>();
                LoadFromXmlStream(XmlStream);
            }
            else
                throw new Exception("Не задан поток, из которого читаются результаты теста");
        }

        /// <summary>
        /// Создает ответ из xml-файла. В файле - ответы, сам тест, информация о студенте и его группе.
        /// </summary>
        /// <param name="XmlFileName"></param>
        public StudentTestAnswer(string XmlFileName)
        {
            if (!String.IsNullOrEmpty(XmlFileName))
            {
                if (System.IO.File.Exists(XmlFileName))
                {
                    FileStream InFile = new FileStream(XmlFileName, FileMode.Open);
                    StudentAnswers = new Dictionary<long, TestQuestionAnswer>();
                    LoadFromXmlStream(InFile);
                }
                else
                    throw new Exception("не существует файл, из которого пытамеся прочитать результаты теста");
            }
            else
                throw new Exception("Не задан тест или студент, проходящий тест");
        }

        /// <summary>
        /// Помечает заданный вариант заданного ответа теста как помеченный правильным студентом
        /// </summary>
        /// <param name="iQuestionOrderNumber">Номер вопроса</param>
        /// <param name="cVariant">Буква варианта</param>
        public void AnswerQuestion(long iQuestionOrderNumber, char cVariant)
        {
            if (iQuestionOrderNumber > 0 && iQuestionOrderNumber <= Test.QuestionNumber)
            {
                if (cVariant >= 'а' && cVariant < ('а' + Test.VariantsInQuestion(((int)iQuestionOrderNumber))))
                {
                    if (StudentAnswers.ContainsKey(iQuestionOrderNumber))
                    {
                        StudentAnswers[iQuestionOrderNumber].AddAnswer(cVariant);
                    }
                    else
                    {
                        StudentAnswers.Add(iQuestionOrderNumber, new TestQuestionAnswer(this, ((TestQuestion)Test[((int)iQuestionOrderNumber - 1)])));
                        StudentAnswers[iQuestionOrderNumber].AddAnswer(cVariant);
                    }
                }
                else
                    throw new Exception("Буква ответа не соответствует ни одному варианту ответа");
            }
            else
                throw new Exception("Неверно указан номер вопроса в последовательности");
        }

        /// <summary>
        /// Указывает, был ли указан студентом заданный вариант ответа заданного вопроса.
        /// </summary>
        /// <param name="iQuestionOrderNumber">Номер вопроса</param>
        /// <param name="cVariant">Буква варианта</param>
        /// <returns></returns>
        public bool AnsweredVariant(long iQuestionOrderNumber, char cVariant)
        {
            bool blRet = false;

            if (iQuestionOrderNumber > 0 && iQuestionOrderNumber <= Test.QuestionNumber)
            {
                if (StudentAnswers.ContainsKey(iQuestionOrderNumber))
                    blRet = StudentAnswers[iQuestionOrderNumber].ContainAnswer(cVariant);
            }
            else
                throw new Exception("Неверно указан номер вопроса");

            return blRet;
        }

        /// <summary>
        /// Снимает ответ студента на заданный вариант заданного вопроса.
        /// </summary>
        /// <param name="iQuestionOrderNumber">Номер вопроса</param>
        /// <param name="cVariant">Номер вараинта</param>
        public void DoNotAnswerQuestion(long iQuestionOrderNumber, char cVariant)
        {
            if (iQuestionOrderNumber > 0 && iQuestionOrderNumber <= Test.QuestionNumber)
            {
                if (cVariant >= 'а' && cVariant < ('а' + Test.VariantsInQuestion(((int)iQuestionOrderNumber))))
                {
                    if (StudentAnswers.ContainsKey(iQuestionOrderNumber))
                    {
                        if (StudentAnswers[iQuestionOrderNumber].ContainAnswer(cVariant))
                            StudentAnswers[iQuestionOrderNumber].RemoveAnswer(cVariant);
                    }
                }
                else
                    throw new Exception("Буква ответа не соответствует ни одному варианту ответа");
            }
            else
                throw new Exception("Неверно указан номер вопроса в последовательности");
        }

        /// <summary>
        /// Сохраняет ответы студента (только ответы!) в xml-узел заданного документа
        /// </summary>
        /// <param name="Document"></param>
        /// <returns></returns>
        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                try
                {
                    XmlElement SANode = Document.CreateElement("StudentAnswer");
                    XmlAttribute Date = Document.CreateAttribute("executiondatetime");
                    Date.Value = Convert.ToString(ExecutionDateTime);
                    SANode.Attributes.Append(Date);
                    XmlAttribute SecondsFromStratFSAttr = Document.CreateAttribute("secondsfromstart");
                    SecondsFromStratFSAttr.Value = Convert.ToString(nSecondsFromStart);
                    SANode.Attributes.Append(SecondsFromStratFSAttr);
                    XmlAttribute CurrQuestionNumAttr = Document.CreateAttribute("currentquestionnum");
                    CurrQuestionNumAttr.Value = Convert.ToString(iCurrentQuestion);
                    SANode.Attributes.Append(CurrQuestionNumAttr);
                    XmlAttribute Rez = Document.CreateAttribute("rightanswerspercent");
                    Rez.Value = Convert.ToString(Test.CalculateResult(this));
                    SANode.Attributes.Append(Rez);
                    XmlAttribute RezBall = Document.CreateAttribute("recievedball");
                    RezBall.Value = Convert.ToString(Test.RecievedBall(this));
                    SANode.Attributes.Append(RezBall);

                    foreach (long iQNum in StudentAnswers.Keys)
                    {
                        SANode.AppendChild(StudentAnswers[iQNum].ExportToXmlNode(Document));
                    }

                    return SANode;
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось экспортировать ответ студента в xml-узел: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан документ, к котоому добавляется узел ответов студента");
        }

        /// <summary>
        /// Загружает из xml-узла.
        /// Загрузка не меняет базовый тест и базового студента!!!
        /// </summary>
        /// <param name="Node"></param>
        public override void LoadFromXmlNode(XmlNode Node)
        {
            if (Node != null)
            {
                try
                {
                    ExecutionDateTime = Convert.ToDateTime(Node.Attributes["executiondatetime"].Value);
                }
                catch
                {
                }
                try
                {
                    nSecondsFromStart = Convert.ToInt32(Node.Attributes["secondsfromstart"].Value);
                }
                catch
                {
                }
                try
                {
                    iCurrentQuestion = Convert.ToInt32(Node.Attributes["currentquestionnum"].Value);
                }
                catch
                {
                }

                try
                {
                    StudentAnswers.Clear();
                    foreach (XmlNode tqa in Node.SelectNodes("TestQuestionAnswer"))
                    {
                        foreach(XmlNode lt in tqa.SelectNodes("AnsweredLetter"))
                            AnswerQuestion(Convert.ToInt64(tqa.Attributes["TestOrderQuestionNumber"].Value), Convert.ToChar(lt.Attributes["letter"].Value));
                    }
                }
                catch (Exception e1)
                {
                    throw new Exception("Не удалось считать тестирование студента из xml-узла: " + e1.Message, e1);
                }
            }
            else
                throw new Exception("Не задан узел ответов студента на тест");
        }

        /// <summary>
        /// Сохраняет в поток в виде xml.
        /// Записывает так же информацию о студенте (и его группе) и сам тест, а не только ответы на него.
        /// </summary>
        /// <param name="Stream"></param>
        public override void SaveToXmlStream(Stream Stream)
        {
            XmlDocument Doc = new XmlDocument();
            XmlElement STTest = Doc.CreateElement("StudentTest");

            XmlNode StudentNode = Student.ExportToXmlNode(Doc);
            StudentNode.AppendChild(Student.Group.ExportToXmlNode(Doc));

            STTest.AppendChild(StudentNode);
            STTest.AppendChild(Test.ExportToXmlNode(Doc));
            STTest.AppendChild(this.ExportToXmlNode(Doc));
            Doc.AppendChild(STTest);

            Doc.Save(Stream);
        }

        /// <summary>
        /// Загружает информацию о прохождении теста из xml-потока.
        /// Внимание! Замещает информацию о родительском тесте, 
        /// студенте и его группе внутри данного объекта!
        /// </summary>
        /// <param name="Stream"></param>
        public override void LoadFromXmlStream(Stream Stream)
        {
            XmlDocument Doc = new XmlDocument();
            Doc.Load(Stream);

            XmlNode StudentNode=Doc.SelectSingleNode("StudentTest/Student");
            Group CurGroup = new Group("_", "_", 1991);
            XmlNode GroupNode = StudentNode.SelectSingleNode("Group");
            CurGroup.LoadFromXmlNode(GroupNode);
            Student = new Student(StudentNode, CurGroup);

            XmlNode TestNode = Doc.SelectSingleNode("StudentTest/Test");
            Test = new Test(1, "_", "_", "_", -1);
            Test.LoadFromXmlNode(TestNode);

            XmlNode TestAnswerNode = Doc.SelectSingleNode("StudentTest/StudentAnswer");
            LoadFromXmlNode(TestAnswerNode);
        }
    }

    /// <summary>
    /// Ответ студента на вопрос теста-попытки.
    /// </summary>
    public class TestQuestionAnswer:BaseObject
    {
        protected StudentTestAnswer StudentTestAnswer;

        protected TestQuestion Question;
        protected List<char> AnsweredLetters;

        public TestQuestion ParentQuestion
        {
            get { return Question; }
        }
        public StudentTestAnswer ParentAnswer
        {
            get { return StudentTestAnswer; }
        }
        public char[] AnswerLetters
        {
            get { return AnsweredLetters.ToArray(); }
        }

        public TestQuestionAnswer(StudentTestAnswer StudentAnswer, TestQuestion AnsweringQuestion)
        {
            if (StudentAnswer != null && AnsweringQuestion != null)
            {
                StudentTestAnswer = StudentAnswer;
                Question = AnsweringQuestion;

                AnsweredLetters = new List<char>();
            }
            else
                throw new Exception("Не задан ответ студента или вопрос");
        }

        public void AddAnswer(char cAnswer)
        {
            if (!AnsweredLetters.Contains(cAnswer))
                AnsweredLetters.Add(cAnswer);
        }

        public bool ContainAnswer(char cVariant)
        {
            return AnsweredLetters.Contains(cVariant);
        }

        public void RemoveAnswer(char cAnswer)
        {
            if (AnsweredLetters.Contains(cAnswer))
                AnsweredLetters.Remove(cAnswer);
        }

        public override XmlNode ExportToXmlNode(XmlDocument Document)
        {
            if (Document != null)
            {
                XmlElement TQANode = Document.CreateElement("TestQuestionAnswer");
                XmlAttribute QNum = Document.CreateAttribute("TestOrderQuestionNumber");
                QNum.Value = Convert.ToString(Question.OrderQuestionNumber);
                TQANode.Attributes.Append(QNum);

                foreach (char c in AnsweredLetters)
                {
                    XmlElement AnsweredLetterNode = Document.CreateElement("AnsweredLetter");
                    XmlAttribute lt = Document.CreateAttribute("letter");
                    lt.Value = Convert.ToString(c);
                    AnsweredLetterNode.Attributes.Append(lt);

                    TQANode.AppendChild(AnsweredLetterNode);
                }

                return TQANode;
            }
            else
                throw new Exception("Не задан документ, к которому будет добавлен узел");
        }

        public override void LoadFromXmlNode(XmlNode Node)
        {
            throw new NotImplementedException();
        }
    }
}