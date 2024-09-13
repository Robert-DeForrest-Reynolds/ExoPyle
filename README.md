You'll need Python installed to use this editor. [Python](https://www.python.org/downloads/)

### Windows Installation
Download most recent release, extract the ExoFyle directory where you'd like.

Open a command prompt as admin, navigate to the ExoFyle directory, and run the bat script using the command below.
You need to open as admin because it will add the directory to your path so you can open ExoFyle using the command exo.bat

```bat
cd C:\
mkdir C:\ExoFyleVenv & cd C:\ExoFyleVenv
py -m venv Venv & Venv\Scripts\activate & pip install raylib-py & deactivate
cd ..
mkdir ExoFyle & cd ExoFyle
curl -L -o exofyle.zip https://github.com/Robert-DeForrest-Reynolds/ExoFyle/releases/download/0.0.3/Alpha_0.0.3.zip
tar -xf ExoFyle.zip
del ExoFyle.zip
setx /M PATH "%PATH%;C:\ExoFyle"
cd C:\ & exo.bat
```

### Linux Installation
You should probably just download [NeoVim](https://neovim.io/) honestly, but uh, in case you really want it:

```bash
./Setup.sh
```

I suggest adding an alias that opens it.

---

Warning, I use profanity.

### Reasoning
I have two computers, one runs Windows, and the other run Linux. My Windows laptop is my multi-monitor workstation for home, and my Linux laptop is my portable solution for working on the go. Ironically, I'm much faster on my Linux laptop because of, you guessed it, NeoVim, and Linux's customizability. I have hundreds of aliases, and scripts.

Windows is downright uncustomizable. This is not a skill issue, this is a critique. I'm well aware of the likes of implements that attempt to bridge this gap, and some have done really well, others *cough* PowerToys *cough* have done rather poorly considering their native development. In short, I have found myself quite discontent with the Windows development environments. So, I began a journey in creating tooling for developers to work with on Windows that at minimum attempts to leave bloat at the door.

Here's the thing though, low-level complication will never help high-level learning. We want new programmer's to learn fast, and well. We cannot simply expect them to learn in 2-4 years, even weeks sometimes, what took the previous generation 10+ years to learn. Programming isn't just about knowledge, it's about practice, and tooling as well. This shit takes years to get good at, especially when the tools are fundamental difficult for a normal ass human to learn. I don't think people choose VSCode over Neovim because they think VSCode is better, I think they think it's easier. My fundamental goal with this text editor was:
 - What programming languages are complete beginners preferring to be learn currently? I'm not going to sugar coat it, I'm not using JavaScript, so, Python it is.
 - What is the biggest quarrel of the "real", gigachad developers when it comes to VSCode, and Visual Studio? *(that I've observed)* Extensibility, and performance; monolithic nature. Alright, we're working with Python, but I think I got this, and monoliths are pretty, but I don't have an obsession with them, so I think we can avoid that.
 - What is *my* preferred programming language to teach, and what is my biggest quarrel with VSCode and Visual Studio? Python, extensibility, and performance. (I'm not a real developer by the way. Real developers use Linux, and TypeScript I hear)


*Hey, I'm Irish, I get to be a little cheeky*


### Design Pillars
 - Very little batteries included.
 - Extensive API
 - Fast Enough, I'm Not Here to Replace NeoVim
 - Minimal UI Design, Minimal Focus Lost

### Extending
To extend, create a Python script within the `Packages` directory, within the directory that ExoFyle is located. If you downloaded an official release, it'll come with an empty package directory within the directory. There is also a `PackageExamples` directory with examples if interacting with the API.
If you're familiar with Python, simply reading first chapter of the [documentation](https://github.com/Robert-DeForrest-Reynolds/ExoFyle/wiki/ExoFyle-Documentation) will help you get up to speed if I've done my job well.