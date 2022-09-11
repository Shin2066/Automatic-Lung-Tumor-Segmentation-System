using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using Dicom;
using System.Threading;
using System.Drawing;

namespace test1
{
    public partial class Form3 : Form
    {
        public static Form3 instance;
        public ListView LV1;
        public static int i; //讀入幾張圖
        public string str;
        public string filepath= @"D:\UI\";  //修改此路徑
        public string pythonpath = @"C:\Users\iris-yuntech\anaconda3\envs\pytorch\python.exe";//修改此路徑
        public string labelme = @"C:\Users\iris-yuntech\anaconda3\envs\labelme\Scripts\labelme.exe";//修改此路徑
        public Form3()
        {
            InitializeComponent();

            instance = this;
            LV1 = listView1;

        }

        private void Form3_Load(object sender, EventArgs e)
        {

        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            /*
            //read data
            using (OpenFileDialog ofd = new OpenFileDialog() { Filter = "All files|*.*", ValidateNames = true, Multiselect = true })
            {
                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    foreach (string f in ofd.FileNames)
                    {
            */

            // 執行檔路徑下的 MyDir 資料夾
            try
            {
                FolderBrowserDialog dialog = new FolderBrowserDialog();
                dialog.Description = "請選擇dicom所在資料夾";
                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    if (string.IsNullOrEmpty(dialog.SelectedPath))
                    {
                        MessageBox.Show(this, "資料夾路徑不能為空", "提示");
                        return;
                    }

                    //MessageBox.Show(dialog.SelectedPath);
                    string folderName = dialog.SelectedPath;
                    //string folderName = @"D:\UI\CAT-UNet\dcm_data";
                    // 取得資料夾內所有檔案
                    File.WriteAllText(filepath+@"CAT-UNet\temp\path.txt", folderName);
                    foreach (string f in Directory.GetFiles(folderName))
                    {
                        FileInfo fi = new FileInfo(f);
                        ListViewItem item = new ListViewItem(fi.Name);
                        listView1.Items.Add(item);

                        string Dicomimage = f;
                        DicomFile dcmFile = DicomFile.Open(Dicomimage);
                        DicomDataset dcmDataset = dcmFile.Dataset;
                        //DicomFileMetaInformation dcmMetaInfo = dcmFile.FileMetaInfo;
                        string patientID = dcmDataset.Get(DicomTag.PatientID, ""); //dicom tag
                        item.SubItems.Add(patientID);

                        item.SubItems.Add(fi.FullName);  //path路徑


                        //string[] lines = File.ReadAllLines(@"D:\UI\CAT-UNet\temp\output.txt");
                        //for (int line = 0; line < lines.Length; line++)
                        //{
                        //item.SubItems.Add(lines[i]);  //影像預測結果(load data報錯)
                        item.SubItems.Add("");
                        //Form1 f1 = new Form1();
                        item.SubItems.Add("");  //醫生判斷結果
                        //}
                        i++; //影像total數量
                    }
                    textBox8.Text = Convert.ToString(i);
                    /*
                    string[] totals = File.ReadAllLines(@"D:\UI\CAT-UNet\temp\total.txt");
                    for (int total = 0; total < totals.Length; total++)
                    {
                        textBox3.Text = Convert.ToString(totals[1]);
                        textBox4.Text = Convert.ToString(totals[2]);
                    }
                    */
                    label17.Text = "Please Predict Data";
                    label17.ForeColor = Color.Green;
                    }
            }
            catch (Exception ee) { }
        }

        private void label6_Click(object sender, EventArgs e)
        {

        }

        private void label12_Click(object sender, EventArgs e)
        {

        }

        private void Form3_TextChanged(object sender, EventArgs e)
        {
            //搜尋事件
        }

        private void button6_Click(object sender, EventArgs e)
        {
            //select

            Form1 f = new Form1();
            f.Visible = true;
            f.Visible = true;
        }

        private void button3_Click(object sender, EventArgs e)
        {
            //search
            listView1.SelectedItems.Clear();
            for (int x = listView1.Items.Count - 1; x >= 0; x--)
            {
                if (listView1.Items[x].SubItems[0].ToString().ToLower().Contains(textBox1.Text.ToLower()))
                {
                    listView1.Items[x].Selected = true;
                    listView1.Select();
                }
                if (listView1.Items[x].SubItems[1].ToString().ToLower().Contains(textBox1.Text.ToLower()))
                {
                    listView1.Items[x].Selected = true;
                    listView1.Select();
                }
                if (listView1.Items[x].SubItems[2].ToString().ToLower().Contains(textBox1.Text.ToLower()))
                {
                    listView1.Items[x].Selected = true;
                    listView1.Select();
                }
                if (listView1.Items[x].SubItems[3].ToString().ToLower().Contains(textBox1.Text.ToLower()))
                {
                    listView1.Items[x].Selected = true;
                    listView1.Select();
                }
                if (listView1.Items[x].SubItems[4].ToString().ToLower().Contains(textBox1.Text.ToLower()))
                {
                    listView1.Items[x].Selected = true;
                    listView1.Select();
                }
            }
        }

        private void button5_Click(object sender, EventArgs e)
        {
            //show dicom test

        }

        private void listView1_MouseClick(object sender, MouseEventArgs e)
        {
            //String selected = listView1.SelectedItems[0].SubItems[1].Text;
            //MessageBox.Show(selected);
            Form1 form = new Form1();
            form.Show();
        }

        private void textBox8_TextChanged(object sender, EventArgs e)
        {
            //system result total

        }

        private void textBox3_TextChanged(object sender, EventArgs e)
        {

        }
        private void run_cmd()
        {


            string fileName = filepath+@"CAT-UNet\run2.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(pythonpath, fileName)
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();

            Console.WriteLine(output);

            Console.ReadLine();

            MessageBox.Show("Prediction Complete","Message");

        }

        private void run_cmd2()
        {


            string fileName = filepath + @"CAT-UNet\run2.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(pythonpath, fileName)
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();

            Console.WriteLine(output);

            Console.ReadLine();

            MessageBox.Show("Prediction Complete", "Message");

        }

        private void button2_Click(object sender, EventArgs e)
        {
            label17.Text = "Processing...";
            label17.ForeColor = Color.Red;
            Task thread1 = Task.Factory.StartNew(() => run_cmd());
            //Thread A = new Thread(run_cmd);//指派工作給執行緒
            //A.Start();//使用thread.Start(); 來開始執行緒工作 
            Task.WaitAll(thread1);
            //讀text
            string[] lines = File.ReadAllLines(filepath+@"CAT-UNet\temp\output.txt");
            for (int line = 0; line < lines.Length; line++)
            {
                listView1.Items[line].SubItems[3].Text = (lines[line]);  //影像預測結果(load data報錯)
                //listView1.Items[x].SubItems[3].Text("");  //醫生判斷結果
            }
            string[] totals = File.ReadAllLines(filepath+@"CAT-UNet\temp\total.txt");
            for (int total = 0; total < totals.Length; total++)
            {
                textBox3.Text = Convert.ToString(totals[1]);
                textBox4.Text = Convert.ToString(totals[2]);
            }
            //
            label17.ForeColor = Color.Green;
            label17.Text = "Complete";

        }
        private void groupBox2_Enter(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }


        private void button4_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog ofd = new OpenFileDialog() { Filter = "DCM File| *.dcm", ValidateNames = true, Multiselect = false }) //只讀入dcm檔案
            {
                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    foreach (string f in ofd.FileNames)
                    {
                        File.WriteAllText(filepath + @"CAT-UNet\temp\path.txt", f);
                        FileInfo fi = new FileInfo(f);
                        ListViewItem item = new ListViewItem(fi.Name);
                        listView1.Items.Add(item);
                        string Dicomimage = f;
                        DicomFile dcmFile = DicomFile.Open(Dicomimage);
                        DicomDataset dcmDataset = dcmFile.Dataset;
                        //DicomFileMetaInformation dcmMetaInfo = dcmFile.FileMetaInfo;
                        string patientID = dcmDataset.Get(DicomTag.PatientID, ""); //dicom tag
                        item.SubItems.Add(patientID);

                        item.SubItems.Add(fi.FullName);  //path路徑


                        //string[] lines = File.ReadAllLines(@"D:\UI\CAT-UNet\temp\output.txt");
                        //for (int line = 0; line < lines.Length; line++)
                        //{
                        //item.SubItems.Add(lines[i]);  //影像預測結果(load data報錯)
                        item.SubItems.Add("");
                        //Form1 f1 = new Form1();
                        item.SubItems.Add("");  //醫生判斷結果
                                                //}
                        if (listView1.Items.Count > 1)
                        {
                            listView1.Items.Remove(listView1.Items[0]);
                        }
                        i = 1; //每次只讀一張
                        textBox8.Text = Convert.ToString(i);
                        label17.Text = "Please Predict Data";
                        label17.ForeColor = Color.Green;
                    }
                }

            }
        }
        private void button5_Click_1(object sender, EventArgs e)
        {
            double n_to_m =0 ;
            double m_to_n = 0;
            double check_total = 0;
            //MessageBox.Show(Convert.ToString(listView1.SelectedItems[1].SubItems[4].Text));
            for (int x = listView1.Items.Count-1; x>=0; x--)
            {
                if (listView1.Items[x].SubItems[4].Text != "")
                {
                    check_total += 1;
                    if (listView1.Items[x].SubItems[3].Text != listView1.Items[x].SubItems[4].Text)
                    {
                        if (listView1.Items[x].SubItems[3].Text == "Normal" )
                        {
                            n_to_m += 1;
                        }
                        else if (listView1.Items[x].SubItems[3].Text == "Mass" )
                        {
                            m_to_n += 1;
                        }
                    }

                    textBox5.Text = Convert.ToString(n_to_m);
                    textBox7.Text = Convert.ToString(m_to_n);
                    textBox6.Text = Convert.ToString(check_total);
                    textBox9.Text = Convert.ToString((((check_total - (n_to_m + m_to_n)) / check_total)) * 100);
                }
                
            }
        }

        private void Form3_KeyDown(object sender, KeyEventArgs e)
        {

        }

        private void listView1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                Form1 form = new Form1();
                form.Show();
            }
        }
    }
}
