using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace test1
{
    public partial class Form1 : Form
    {
        public static Form1 instance;
        public Form1()
        {
            InitializeComponent();
            instance = this;
            //show pic1 image
            String selected = Form3.instance.LV1.SelectedItems[0].SubItems[2].Text;
            //MessageBox.Show(Path.GetFileNameWithoutExtension(selected) + ".bmp");
            pictureBox1.Image = Image.FromFile(Form3.instance.filepath+@"x_rays\val\images\" + Path.GetFileNameWithoutExtension(selected) + ".bmp");
            pictureBox2.Image = Image.FromFile(Form3.instance.filepath+@"result\" + Path.GetFileNameWithoutExtension(selected) + ".bmp");
            label1.Text = ("Original= "+ Form3.instance.filepath+@"x_rays_data\val\images\" + Path.GetFileNameWithoutExtension(selected) + ".bmp");
            label3.Text = ("Prediction= "+ Form3.instance.filepath+@"result\" + Path.GetFileNameWithoutExtension(selected) + ".bmp");
        }


        int i = 0;
        //下一张
        private void button6_Click(object sender, EventArgs e)
        {
            //***資料夾沒影像會報錯
            string[] path = Directory.GetFiles(@"D:\UI\CAT-UNet\x_rays_data\val\images\");
            string[] path2 = Directory.GetFiles(@"D:\UI\CAT-UNet\result\");
            //每点一下，i++，path[i]指向下一张图片
            i++;
            if (i > path.Length - 1)
            {
                i = 0;//到最后一张，返回第一张
            }
            pictureBox1.Image = Image.FromFile(path[i]);
            pictureBox2.Image = Image.FromFile(path2[i]);
            label1.Text = "FileName = " + (path[i]);
            label3.Text = "FileName = " + (path2[i]);

        }
        //上一张
        private void button5_Click(object sender, EventArgs e)
        {
            string[] path = Directory.GetFiles(@"D:\UI\CAT-UNet\x_rays_data\val\images\");
            string[] path2 = Directory.GetFiles(@"D:\UI\CAT-UNet\result\");
            i--;
            if (i < 0)
            {
                i = path.Length - 1;
            }
            pictureBox1.Image = Image.FromFile(path[i]);
            pictureBox2.Image = Image.FromFile(path2[i]);
            label1.Text = "FileName = " + (path[i]);
            label3.Text = "FileName = " + (path2[i]);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //窗体加载时，显示一张图片
            this.KeyPreview = true; //鍵盤事件開啟

        }



        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }




        private void button4_Click(object sender, EventArgs e)
        {
            //呼叫label_me
            Process p = Process.Start(Form3.instance.labelme);
            p.WaitForExit();
        }


        private void folderBrowserDialog1_HelpRequest(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void button9_Click(object sender, EventArgs e)
        {
             //NG
            string NGpath = this.label1.Text;
            string filename2 = null;
            filename2 = Path.GetFileName(NGpath);
            Console.WriteLine(filename2);
            Console.ReadLine();
            DialogResult dialogResult = MessageBox.Show("Do you want to save this image to NG?", "Message", MessageBoxButtons.YesNo);
            if (dialogResult == DialogResult.Yes)
            {
                try
                {
                    string line1 = File.ReadLines(Form3.instance.filepath + @"CAT-UNet\temp\path.txt").First(); // gets the first line from file.

                    string sourceFile_images = Form3.instance.filepath+@"x_rays\val\images\" + filename2;
                    string sourceFile_dicom = line1 + "/"+ Path.GetFileNameWithoutExtension(filename2)+ ".dcm";
                    string destinationFile = Form3.instance.filepath + @"CAT-UNet\NG\" + filename2;
                    string destinationFile2 = Form3.instance.filepath + @"CAT-UNet\NG\"+Path.GetFileNameWithoutExtension(filename2) + ".dcm";
                    File.Copy(Path.Combine(sourceFile_images), Path.Combine(destinationFile));
                    File.Copy(Path.Combine(sourceFile_dicom), Path.Combine(destinationFile2));
                    //System.IO.File.Move(sourceFile, destinationFile);
                    MessageBox.Show(filename2 + " is saved");
                }

                catch (Exception ee) { MessageBox.Show(filename2 + " had been saved"); }
            }
            else if (dialogResult == DialogResult.No)
            {
                //do something else
            }

        }


        private void button10_Click(object sender, EventArgs e)
        {
            
            //run_label_cmd();
        }
        private void run_label_cmd()
        {

            string fileName = @"D:\UI\CAT-UNet\labelme\labelme_run.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(@"C:\Users\iris-yuntech\anaconda3\envs\pytorch\python.exe", fileName)
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

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            //check_total += 1;
            Form3.instance.str = comboBox1.Text;

            Form3.instance.LV1.SelectedItems[0].SubItems[4].Text = Form3.instance.str;
            
            if (Form3.instance.LV1.SelectedItems[0].SubItems[3].Text != Form3.instance.LV1.SelectedItems[0].SubItems[4].Text)
            {
                //button9.PerformClick();
                DialogResult dialogResult = MessageBox.Show("Do you want to save this image to NG?", "Message", MessageBoxButtons.YesNo);
                if (dialogResult == DialogResult.Yes)
                {
                    button9.PerformClick();
                }
                else if (dialogResult == DialogResult.No)
                {
                    //do something else
                }
            }

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.PageDown)
            {
                comboBox1.DroppedDown = true;
            }

            if (e.KeyCode == Keys.Right || e.KeyCode == Keys.Enter)
            {
                e.SuppressKeyPress = true;
                SendKeys.Send("{TAB}");
            }
            else if (e.KeyCode == Keys.Left)
            {
                e.SuppressKeyPress = true;
                SendKeys.Send("+{TAB}");

            }
        }

            private void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (char)Keys.Escape)
            {
                this.Close();
            }
        }
    }
}
