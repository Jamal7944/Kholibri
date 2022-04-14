Imports System.IO.Compression
Imports System.Net

Public Class FormInstaller
    Dim KhollibriUrl As String = "https://github.com/Jamal7944/Kholibri/archive/refs/heads/main.zip"
    Dim Python3Url As String = "https://www.python.org/ftp/python/3.10.4/python-3.10.4-embed-amd64.zip"
    Dim TeXLiveUrl As String = "https://mirror.ctan.org/systems/texlive/tlnet/install-tl-windows.exe"
    Dim wc As WebClient
    Private Sub FormInstaller_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        TbKhollibri_Leave(sender, e)
        TbPython3_Leave(sender, e)
        TbTeXLive_Leave(sender, e)

        TbKhollibri.Text = My.Settings.KhollibriPath
        TbPython3.Text = My.Settings.Python3Path
        TbTeXLive.Text = My.Settings.TeXLivePath

        wc = New WebClient()
        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls Or SecurityProtocolType.Tls11 Or SecurityProtocolType.Tls12 Or SecurityProtocolType.Ssl3
    End Sub

    Private Sub TbKhollibri_Enter(sender As Object, e As EventArgs) Handles TbKhollibri.Enter
        If TbKhollibri.Text = "Chemin vers le répertoire d'installation de Khollibri" Then
            TbKhollibri.Text = String.Empty
        End If
    End Sub

    Private Sub TbKhollibri_Leave(sender As Object, e As EventArgs) Handles TbKhollibri.Leave
        If TbKhollibri.Text = String.Empty Then
            TbKhollibri.Text = "Chemin vers le répertoire d'installation de Khollibri"
        End If
    End Sub

    Private Sub TbPython3_Enter(sender As Object, e As EventArgs) Handles TbPython3.Enter
        If TbPython3.Text = "Chemin vers le répertoire d'installation de Python 3" Then
            TbPython3.Text = String.Empty
        End If
    End Sub

    Private Sub TbPython3_Leave(sender As Object, e As EventArgs) Handles TbPython3.Leave
        If TbPython3.Text = String.Empty Then
            TbPython3.Text = "Chemin vers le répertoire d'installation de Python 3"
        End If
    End Sub

    Private Sub TbTeXLive_Enter(sender As Object, e As EventArgs) Handles TbTeXLive.Enter
        If TbTeXLive.Text = "Chemin vers le répertoire d'installation de TeX Live" Then
            TbTeXLive.Text = String.Empty
        End If
    End Sub

    Private Sub TbTeXLive_Leave(sender As Object, e As EventArgs) Handles TbTeXLive.Leave
        If TbTeXLive.Text = String.Empty Then
            TbTeXLive.Text = "Chemin vers le répertoire d'installation de TeX Live"
        End If
    End Sub

    Private Sub CbInstallKhollibri_CheckedChanged(sender As Object, e As EventArgs) Handles CbInstallKhollibri.CheckedChanged
        TbKhollibri.Enabled = CbInstallKhollibri.Checked
        BtnBrowseKhollibri.Enabled = CbInstallKhollibri.Checked
    End Sub

    Private Sub CbInstallPython3_CheckedChanged(sender As Object, e As EventArgs) Handles CbInstallPython3.CheckedChanged
        TbPython3.Enabled = CbInstallPython3.Checked
        BtnBrowsePython3.Enabled = CbInstallPython3.Checked
    End Sub

    Private Sub CbInstallTeXLive_CheckedChanged(sender As Object, e As EventArgs) Handles CbInstallTeXLive.CheckedChanged
        TbTeXLive.Enabled = CbInstallTeXLive.Checked
        BtnBrowseTeXLive.Enabled = CbInstallTeXLive.Checked
    End Sub

    Private Sub BtnBrowseKhollibri_Click(sender As Object, e As EventArgs) Handles BtnBrowseKhollibri.Click
        If FbdKhollibri.ShowDialog() = DialogResult.OK Then
            TbKhollibri.Text = FbdKhollibri.SelectedPath
        End If
    End Sub

    Private Sub BtnBrowsePython3_Click(sender As Object, e As EventArgs) Handles BtnBrowsePython3.Click
        If FbdPython3.ShowDialog() = DialogResult.OK Then
            TbPython3.Text = FbdPython3.SelectedPath
        End If
    End Sub

    Private Sub BtnBrowseTeXLive_Click(sender As Object, e As EventArgs) Handles BtnBrowseTeXLive.Click
        If FbdTeXLive.ShowDialog() = DialogResult.OK Then
            TbTeXLive.Text = FbdTeXLive.SelectedPath
        End If
    End Sub

    Private Sub BtnInstall_Click(sender As Object, e As EventArgs) Handles BtnInstall.Click
        Dim unit = Math.Abs(100 / (CbInstallKhollibri.Checked + CbInstallPython3.Checked + CbInstallTeXLive.Checked))
        If CbInstallKhollibri.Checked Then
            If TbKhollibri.Text <> String.Empty And My.Computer.FileSystem.DirectoryExists(TbKhollibri.Text) Then
                Download(KhollibriUrl, TbKhollibri.Text + "\main.zip")
                ProgressBar1.Value += unit
            Else
                MessageBox.Show("Veuillez spécifier un chemin d'installation valide pour Khôlibri.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error)
                Return
            End If
        End If
        If CbInstallPython3.Checked Then
            If TbPython3.Text <> String.Empty And My.Computer.FileSystem.DirectoryExists(TbPython3.Text) Then
                Download(Python3Url, TbPython3.Text + "\python-3.10.4-embed-amd64.zip")
                ProgressBar1.Value += unit
            Else
                MessageBox.Show("Veuillez spécifier un chemin d'installation valide pour Python 3.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error)
                Return
            End If
        End If
        If CbInstallTeXLive.Checked Then
            If TbTeXLive.Text <> String.Empty And My.Computer.FileSystem.DirectoryExists(TbTeXLive.Text) Then
                Download(TeXLiveUrl, TbTeXLive.Text + "\install-tl.exe", False)
                ProgressBar1.Value += unit
                Process.Start(TbTeXLive.Text + "\install-tl.exe")
            Else
                MessageBox.Show("Veuillez spécifier un chemin d'installation valide pour TeX Live.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error)
                Return
            End If
        End If
        ProgressBar1.Value = 0
        MessageBox.Show("Téléchargement terminé")
        Close()
    End Sub

    Private Sub FormInstaller_FormClosing(sender As Object, e As FormClosingEventArgs) Handles MyBase.FormClosing
        My.Settings.KhollibriPath = TbKhollibri.Text
        My.Settings.Python3Path = TbPython3.Text
        My.Settings.TeXLivePath = TbTeXLive.Text
        My.Settings.Save()
    End Sub

    Private Sub Download(url As String, fileName As String, Optional Unzip As Boolean = True)
        Try
            wc.DownloadFile(url, fileName)
            If Unzip Then
                ZipFile.ExtractToDirectory(fileName, fileName.Replace(".zip", ""))
                My.Computer.FileSystem.DeleteFile(fileName)
            End If
        Catch ex As Exception
            MessageBox.Show(ex.Message, "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
    End Sub
End Class
