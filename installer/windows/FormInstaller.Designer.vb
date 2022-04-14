<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class FormInstaller
    Inherits System.Windows.Forms.Form

    'Form remplace la méthode Dispose pour nettoyer la liste des composants.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Requise par le Concepteur Windows Form
    Private components As System.ComponentModel.IContainer

    'REMARQUE : la procédure suivante est requise par le Concepteur Windows Form
    'Elle peut être modifiée à l'aide du Concepteur Windows Form.  
    'Ne la modifiez pas à l'aide de l'éditeur de code.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Me.LblTitle = New System.Windows.Forms.Label()
        Me.GbOptions = New System.Windows.Forms.GroupBox()
        Me.ProgressBar1 = New System.Windows.Forms.ProgressBar()
        Me.BtnInstall = New System.Windows.Forms.Button()
        Me.BtnBrowseTeXLive = New System.Windows.Forms.Button()
        Me.BtnBrowsePython3 = New System.Windows.Forms.Button()
        Me.BtnBrowseKhollibri = New System.Windows.Forms.Button()
        Me.TbPython3 = New System.Windows.Forms.TextBox()
        Me.TbKhollibri = New System.Windows.Forms.TextBox()
        Me.CbInstallKhollibri = New System.Windows.Forms.CheckBox()
        Me.CbInstallTeXLive = New System.Windows.Forms.CheckBox()
        Me.CbInstallPython3 = New System.Windows.Forms.CheckBox()
        Me.FbdKhollibri = New System.Windows.Forms.FolderBrowserDialog()
        Me.FbdPython3 = New System.Windows.Forms.FolderBrowserDialog()
        Me.FbdTeXLive = New System.Windows.Forms.FolderBrowserDialog()
        Me.TbTeXLive = New System.Windows.Forms.TextBox()
        Me.GbOptions.SuspendLayout()
        Me.SuspendLayout()
        '
        'LblTitle
        '
        Me.LblTitle.Dock = System.Windows.Forms.DockStyle.Top
        Me.LblTitle.Font = New System.Drawing.Font("Microsoft Sans Serif", 36.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LblTitle.Location = New System.Drawing.Point(0, 0)
        Me.LblTitle.Name = "LblTitle"
        Me.LblTitle.Size = New System.Drawing.Size(782, 69)
        Me.LblTitle.TabIndex = 0
        Me.LblTitle.Text = "Installateur Khôlibri"
        Me.LblTitle.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'GbOptions
        '
        Me.GbOptions.Controls.Add(Me.ProgressBar1)
        Me.GbOptions.Controls.Add(Me.BtnInstall)
        Me.GbOptions.Controls.Add(Me.BtnBrowseTeXLive)
        Me.GbOptions.Controls.Add(Me.BtnBrowsePython3)
        Me.GbOptions.Controls.Add(Me.BtnBrowseKhollibri)
        Me.GbOptions.Controls.Add(Me.TbTeXLive)
        Me.GbOptions.Controls.Add(Me.TbPython3)
        Me.GbOptions.Controls.Add(Me.TbKhollibri)
        Me.GbOptions.Controls.Add(Me.CbInstallKhollibri)
        Me.GbOptions.Controls.Add(Me.CbInstallTeXLive)
        Me.GbOptions.Controls.Add(Me.CbInstallPython3)
        Me.GbOptions.Dock = System.Windows.Forms.DockStyle.Fill
        Me.GbOptions.Location = New System.Drawing.Point(0, 69)
        Me.GbOptions.Name = "GbOptions"
        Me.GbOptions.Size = New System.Drawing.Size(782, 164)
        Me.GbOptions.TabIndex = 1
        Me.GbOptions.TabStop = False
        Me.GbOptions.Text = "Options de téléchargement"
        '
        'ProgressBar1
        '
        Me.ProgressBar1.Anchor = CType(((System.Windows.Forms.AnchorStyles.Bottom Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.ProgressBar1.Location = New System.Drawing.Point(6, 109)
        Me.ProgressBar1.Name = "ProgressBar1"
        Me.ProgressBar1.Size = New System.Drawing.Size(770, 23)
        Me.ProgressBar1.TabIndex = 10
        '
        'BtnInstall
        '
        Me.BtnInstall.Dock = System.Windows.Forms.DockStyle.Bottom
        Me.BtnInstall.Location = New System.Drawing.Point(3, 138)
        Me.BtnInstall.Name = "BtnInstall"
        Me.BtnInstall.Size = New System.Drawing.Size(776, 23)
        Me.BtnInstall.TabIndex = 9
        Me.BtnInstall.Text = "Installer"
        Me.BtnInstall.UseVisualStyleBackColor = True
        '
        'BtnBrowseTeXLive
        '
        Me.BtnBrowseTeXLive.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.BtnBrowseTeXLive.Location = New System.Drawing.Point(740, 77)
        Me.BtnBrowseTeXLive.Name = "BtnBrowseTeXLive"
        Me.BtnBrowseTeXLive.Size = New System.Drawing.Size(30, 23)
        Me.BtnBrowseTeXLive.TabIndex = 8
        Me.BtnBrowseTeXLive.Text = "..."
        Me.BtnBrowseTeXLive.UseVisualStyleBackColor = True
        '
        'BtnBrowsePython3
        '
        Me.BtnBrowsePython3.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.BtnBrowsePython3.Location = New System.Drawing.Point(740, 49)
        Me.BtnBrowsePython3.Name = "BtnBrowsePython3"
        Me.BtnBrowsePython3.Size = New System.Drawing.Size(30, 23)
        Me.BtnBrowsePython3.TabIndex = 7
        Me.BtnBrowsePython3.Text = "..."
        Me.BtnBrowsePython3.UseVisualStyleBackColor = True
        '
        'BtnBrowseKhollibri
        '
        Me.BtnBrowseKhollibri.Anchor = CType((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.BtnBrowseKhollibri.Location = New System.Drawing.Point(740, 21)
        Me.BtnBrowseKhollibri.Name = "BtnBrowseKhollibri"
        Me.BtnBrowseKhollibri.Size = New System.Drawing.Size(30, 23)
        Me.BtnBrowseKhollibri.TabIndex = 6
        Me.BtnBrowseKhollibri.Text = "..."
        Me.BtnBrowseKhollibri.UseVisualStyleBackColor = True
        '
        'TbPython3
        '
        Me.TbPython3.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.TbPython3.Location = New System.Drawing.Point(157, 49)
        Me.TbPython3.Name = "TbPython3"
        Me.TbPython3.Size = New System.Drawing.Size(577, 22)
        Me.TbPython3.TabIndex = 4
        '
        'TbKhollibri
        '
        Me.TbKhollibri.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.TbKhollibri.Location = New System.Drawing.Point(157, 21)
        Me.TbKhollibri.Name = "TbKhollibri"
        Me.TbKhollibri.Size = New System.Drawing.Size(577, 22)
        Me.TbKhollibri.TabIndex = 3
        '
        'CbInstallKhollibri
        '
        Me.CbInstallKhollibri.AutoCheck = False
        Me.CbInstallKhollibri.AutoSize = True
        Me.CbInstallKhollibri.Checked = True
        Me.CbInstallKhollibri.CheckState = System.Windows.Forms.CheckState.Checked
        Me.CbInstallKhollibri.Location = New System.Drawing.Point(12, 22)
        Me.CbInstallKhollibri.Name = "CbInstallKhollibri"
        Me.CbInstallKhollibri.Size = New System.Drawing.Size(130, 21)
        Me.CbInstallKhollibri.TabIndex = 2
        Me.CbInstallKhollibri.Text = "Installer Khôlibri"
        Me.CbInstallKhollibri.UseVisualStyleBackColor = True
        '
        'CbInstallTeXLive
        '
        Me.CbInstallTeXLive.AutoSize = True
        Me.CbInstallTeXLive.Checked = True
        Me.CbInstallTeXLive.CheckState = System.Windows.Forms.CheckState.Checked
        Me.CbInstallTeXLive.Location = New System.Drawing.Point(12, 79)
        Me.CbInstallTeXLive.Name = "CbInstallTeXLive"
        Me.CbInstallTeXLive.Size = New System.Drawing.Size(139, 21)
        Me.CbInstallTeXLive.TabIndex = 1
        Me.CbInstallTeXLive.Text = "Installer TeX Live"
        Me.CbInstallTeXLive.UseVisualStyleBackColor = True
        '
        'CbInstallPython3
        '
        Me.CbInstallPython3.AutoSize = True
        Me.CbInstallPython3.Checked = True
        Me.CbInstallPython3.CheckState = System.Windows.Forms.CheckState.Checked
        Me.CbInstallPython3.Location = New System.Drawing.Point(12, 51)
        Me.CbInstallPython3.Name = "CbInstallPython3"
        Me.CbInstallPython3.Size = New System.Drawing.Size(139, 21)
        Me.CbInstallPython3.TabIndex = 0
        Me.CbInstallPython3.Text = "Installer Python 3"
        Me.CbInstallPython3.UseVisualStyleBackColor = True
        '
        'FbdKhollibri
        '
        Me.FbdKhollibri.Description = "Sélectionnez le dossier d'installation de Khollibri"
        '
        'FbdPython3
        '
        Me.FbdPython3.Description = "Sélectionnez le dossier d'installation de Python3"
        '
        'FbdTeXLive
        '
        Me.FbdTeXLive.Description = "Sélectionnez le dossier d'installation de TeX Live"
        '
        'TbTeXLive
        '
        Me.TbTeXLive.Anchor = CType(((System.Windows.Forms.AnchorStyles.Top Or System.Windows.Forms.AnchorStyles.Left) _
            Or System.Windows.Forms.AnchorStyles.Right), System.Windows.Forms.AnchorStyles)
        Me.TbTeXLive.Location = New System.Drawing.Point(157, 77)
        Me.TbTeXLive.Name = "TbTeXLive"
        Me.TbTeXLive.Size = New System.Drawing.Size(577, 22)
        Me.TbTeXLive.TabIndex = 5
        '
        'FormInstaller
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(8.0!, 16.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(782, 233)
        Me.Controls.Add(Me.GbOptions)
        Me.Controls.Add(Me.LblTitle)
        Me.MinimumSize = New System.Drawing.Size(400, 280)
        Me.Name = "FormInstaller"
        Me.ShowIcon = False
        Me.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        Me.Text = "Khollibri Installer"
        Me.GbOptions.ResumeLayout(False)
        Me.GbOptions.PerformLayout()
        Me.ResumeLayout(False)

    End Sub

    Friend WithEvents LblTitle As Label
    Friend WithEvents GbOptions As GroupBox
    Friend WithEvents CbInstallTeXLive As CheckBox
    Friend WithEvents CbInstallPython3 As CheckBox
    Friend WithEvents CbInstallKhollibri As CheckBox
    Friend WithEvents TbPython3 As TextBox
    Friend WithEvents TbKhollibri As TextBox
    Friend WithEvents BtnBrowseTeXLive As Button
    Friend WithEvents BtnBrowsePython3 As Button
    Friend WithEvents BtnBrowseKhollibri As Button
    Friend WithEvents ProgressBar1 As ProgressBar
    Friend WithEvents BtnInstall As Button
    Friend WithEvents FbdKhollibri As FolderBrowserDialog
    Friend WithEvents FbdPython3 As FolderBrowserDialog
    Friend WithEvents FbdTeXLive As FolderBrowserDialog
    Friend WithEvents TbTeXLive As TextBox
End Class
