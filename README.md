ugo
===

Terminal Bookmarks

inspired by workon of virtualenvwrapper

## Installation

Copy this file to your desired bash plugin location and add this to your .bashrc:

	BASHPLUGINSFOLDER=path_to_your_bash_plugins_folder # (e.g.:=~/.bash/plugins)
	[[ -r $BASHPLUGINSFOLDER/ugo.bash ]] && source $BASHPLUGINSFOLDER/ugo.bash


## Info

	usage: ugo [-h] <command>|<project> <options> [-v]

	<TAB> expands commands|projects

	commands ?(<optional>), options:
	 boot <scriptfile> ?<project>
	 conf ?(<project>|<list>)
	 delete <project>, --all
	 help
	 info ?(<project>)
	 list ?(<project>|<conf>)
	 make <project> ?<path> [ boot <scriptfile> ]
	 set <project> ?<path>
 
	hooks:
	~/.ugo/_ugo_conf/
	 pre-make-hook
	 post-make-hook
 
	~/.ugo/<project>/
	 pre-ugo-hook
	 post-ugo-hook
	 pre-delete-hook [only with delete --all]
	 post-delete-hook [only with delete --all]

	bootscripts:
	~/.ugo/_ugo_conf/
	 boot-<name>
