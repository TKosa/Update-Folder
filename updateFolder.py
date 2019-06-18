import os
from utilityFns import *
from tkinter import *
from tkinter.filedialog import askdirectory
src = "C:/Users/Thomas/Desktop/github/Update-Folder/testA"
dst = "C:/Users/Thomas/Desktop/github/Update-Folder/testB"

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.input_frame = InputFrame(self)
        self.output_frame=None

        #TODO add event log
        self.grid(sticky="news")

    def run(self):
        src = self.input_frame.src_row.label.cget("text")
        dst = self.input_frame.dst_row.label.cget("text")
        runBtn = self.input_frame.runBtn
        
        if not os.path.exists(src) or not os.path.exists(dst):
            runBtn.config(text='Error: path or src does not exist')
            return

        if os.path.realpath(dst).find(os.path.realpath(src)) != -1:
            runBtn.config(text='Error: dst is IN src')
            return

        #runBtn.config(text='Running')



        state_dict = {} #Key is path, item is array of dirents
        change_dict = {}
        populate_statedict(dst, state_dict)
        update(src, dst, state_dict, change_dict)

        try:
            self.output_frame.destroy()
        except AttributeError:
            pass
        self.output_frame = OutputFrame(self, dst, state_dict, change_dict)
        self.output_frame.pack(fill=X)



        runBtn.config(text='Run')
        runBtn.config(command=self.run)


class InputFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.src_row = self.SelectDirectoryRow(self, "Set Src", "C:/Users/Thomas/Desktop/github/Update-Folder/testA")
        self.dst_row = self.SelectDirectoryRow(self, "Set Dst", "C:/Users/Thomas/Desktop/github/Update-Folder/testB")

        self.runBtn = Button(self, text="Run", command=master.run)
        self.runBtn.pack()

        self.pack()

    class SelectDirectoryRow(Frame):
        # A frame with a button and label. On button click, user selects directory, which then appears in label.

        def __init__(self, master, btntext="", labeltext=""):
            super().__init__(master)

            self.label = Label(self, text=labeltext, bg="white")
            self.label.pack(padx=5, side=LEFT)

            self.button = Button(self, text=btntext, command=self.onClick)
            self.button.pack(side=LEFT)

            self.pack(fill=X)

        def onClick(self):
            self.label.config(text=askdirectory())


class OutputFrame(Frame):
    #Container for both viewer widgets

    def __init__(self, master, root, dirstate, changes={}):
        super().__init__(master, bg="white")

        self.FV = self.FolderViewer(self, root, dirstate, changes)


    class FolderViewer():
        """
        Shows folder and subfolders after app has run
        Highlights differences
            removed files shown in red, added in green, modified in yellow

        """
        def __init__(self, master, root, dir_state, changes):
            self.master=master
            self.rowNum = 0
            self.addEntries(root, dir_state, changes)

        def addEntries(self, root, dir_state, changes, spaces = 0):
            #str dir: path of directory
            for file in dir_state[root]:
                path = root+'/'+file
                newEntry  = self.Entry(self.master, path, self.rowNum, changes, spaces)
                self.rowNum += 1
                if(os.path.isdir(path)):
                    self.addEntries(path, dir_state, changes, spaces+2)


        class Entry:
            def __init__(self, master, path, rowNum, changes, spaces=0):
                filename = os.path.basename(path)

                # Button to display filetype (file or directory), and to expand/collapse if dir
                # self.button = Button(master)
                # if os.path.isdir(path):
                #     self.button['image'] = closedFolderImage
                # elif os.path.isfile(path):
                #     self.button['image'] = fileImage
                #self.button.grid(row=rowNum, column=0, sticky="W")

                self.filenameLabel = Label(master, text=" "*spaces+filename, bg="white")
                self.filenameLabel.grid(row=rowNum,column=1, sticky="W")
                change = changes.get(path)
                if changes is not None:
                    if change == "remove":
                        self.filenameLabel.configure(fg="red")
                    if change == "copy":
                        self.filenameLabel.configure(fg="green")
                    if change == "mod":
                        self.filenameLabel.configure(fg="orange")




if __name__=="__main__":
    # This version is for desktop
    root = Tk()
    root.title("Update-Folder")

    global fileImage, closedFolderImage, openFolderImage
    fileImage = PhotoImage(file="./res/file.png")
    closedFolderImage = PhotoImage(file="./res/closed_folder.png")
    openFolderImage = PhotoImage(file="./res/open_folder.png")

    app = Application(master=root)
    root.mainloop()
