#!/bin/bash
#
# folder bookmarks for terminal. 
# inspired by workon of virtualenvwrapper
#
# Author Ruben Nicolaides
#
# installation:
#
# copy this file to your desired bash plugin location and add this to your .bashrc:
# BASHPLUGINSFOLDER=path_to_your_bash_plugins_folder # (e.g.:=~/.bash/plugins)
# [[ -r $BASHPLUGINSFOLDER/ugo.bash ]] && source $BASHPLUGINSFOLDER/ugo.bash
#
# use ugo help for more info
#
# Version: 0.3
#
# TODO: Filter and error for wrong options. <ugo kool make> should throw error
# TODO: add option --boot for ugo-hooks, (starting browser only, because of switching to project, sucks)
#
[[ $UGO_HOME == "" ]] && UGO_HOME="$HOME/.ugo"
[[ $UGO_PROFILE == "" ]] && UGO_PROFILE=".profile"
[[ $UGO_CONFDIR == "" ]] && UGO_CONFDIR="_ugo_conf"
[[ -d "$UGO_HOME/$UGO_CONFDIR" ]] || mkdir -p "$UGO_HOME/$UGO_CONFDIR"
[[ $UGO_TRASH == "" ]] && UGO_TRASH=$HOME/.Trash

UGO_COMMANDS=(boot conf help info list make delete set)
UGO_DEBUG="0"

_ugo_help(){
        cat <<HELO
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

HELO

}

_ugo_conf(){

    if [[ "$1" == "list" ]]
        then
        _ugo_list conf
        return
    fi
    
    local pth=""
    [[ $1 != "" ]] && pth="/$1"
    cd $UGO_HOME$pth
}

_ugo_list(){

    local project=$1
    local filter=$2
    
    if [[ $project != "" ]]
        then
        local lspath="$UGO_HOME/"
        case $project in
            "conf")
                lspath+=$UGO_CONFDIR
                ;;
            *)
                lspath+=$project
                ;;
        esac
        
        if [[ $filter != "" ]]
            then            
            ls -lA1 $lspath | awk '{print $9}' | xargs -n1 basename | grep $filter
        else
            ls -lA1 $lspath | awk '{print $9}' | xargs -n1 basename
        fi
                
        return
    fi
    
    ls -d $UGO_HOME/* | grep -v $UGO_CONFDIR >/dev/null 2>&1
    if [ $? -ne "0" ]
        then
        echo "No projects in $UGO_HOME. Use ugo make."
        return 1
    else 
        ls -lA1d $UGO_HOME/* | grep -v $UGO_CONFDIR | awk '{print $9}' | xargs -n1 basename
    fi
}

_ugo_make(){
    
    local l
    let l=${#@}
    if [[ $l > 3 ]]
        then
        echo "Too much args"
        _ugo_help
        return
    fi    

    local project="$1"
    if [[ "$project" == "" ]]
        then
        echo 'No name for project.'
        return
    fi
    local allowed=a-zA-Z0-9_-
    if [[ ! $project =~ ^[$allowed]+$ ]]
        then
        echo "Project name $project is invalid. Allowed: ^[$allowed]+$."
        return
    fi
    
    local ugo_path="$UGO_HOME/$project"
    if [[ -d "$ugo_path" ]]
        then
        echo "Projects exists. Did nothing. Use set."
        return
    fi
    
    local ugo_profile="$ugo_path/$UGO_PROFILE"
    local cur_dir=$(pwd | sed 's/[ .]//g' | awk '{print $9}' | xargs -n1 basename)
        
    local option=$2
    local option_args=$3
    
    local cmd_set="_ugo_set $project"
    local cmd_option=""
    if [[ "$option" != "" ]]
        then
        case $option in
            "boot")
                local scriptname=$option_args
                cmd_option="_ugo_boot $scriptname $project"
                ;;
            *)
                local setpath=$option
                if ! [[ -d $setpath ]]
                    then
                    echo "No valid path for bookmark! : $setpath"
                    echo "Please create directory first, before you want to bookmark it."
                    return 1
                else
                    cmd_set+=" $setpath"
                fi
                ;;               
        esac
    fi

    _ugo_run_hook "$UGO_CONFDIR" "pre-make-hook"

    if [[ $cur_dir != $project ]]
        then
        mkdir $project; cd $project
    fi

    mkdir $ugo_path
    
    $cmd_set
    
    [[ $cmd_option != "" ]] && $cmd_option

    _ugo_run_hook "$UGO_CONFDIR" "post-make-hook"            
}

_ugo_set(){

    local answer
    
    local ugo_setpath=$(pwd)
    local cur_dir=$(pwd | sed 's/[ .]//g' | awk '{print $9}' | xargs -n1 basename)
    local project="$cur_dir"
        
    [[ "$2" != "" ]] && ugo_setpath="$2"
    [[ "$1" != "" ]] && project="$1"

    local ugo_path="$UGO_HOME/$project"
    local ugo_profile="$ugo_path/$UGO_PROFILE"
    
    if [[ "$project" == "$UGO_CONFDIR" ]]
        then
        echo "$project is our configuration directory. Don´t use it as a project."
        return
    fi
    
    if [[ ! -d $ugo_path ]]
        then
        echo "No project: $ugo_path. Use make."
        return
    fi
    
    if [[ -f $ugo_profile ]]
        then
        
        local old_settings=$(cat "$ugo_profile")
        
        echo "Settings in: $ugo_profile"
        echo
        if [[ "$ugo_setpath" == "$old_settings" ]]
            then
            echo "Already project directory. Doing nothing."
            echo
            return
        fi        
        echo "Old project settings: $old_settings"
        echo "New project settings: $ugo_setpath"
        echo
        echo "ACHTUNG! Willst Du das Projekt $project wirklich überschreiben? (Y/N)"
        read answer
        echo

        if [[ $answer != "Y" ]]
            then
            echo "Abbruch"
            return
        fi

        local history="$ugo_profile".history
        echo $old_settings >> $history        
        echo "History of project-settings in $history:"
        echo
        cat "$history"        
    fi
    
    echo "$ugo_setpath" > "$ugo_profile"
    echo "New project settings in $ugo_profile: $(cat "$ugo_profile")"
    echo    
}

_ugo_delete(){
    
    local answer
    
    local l
    let l=${#@}
    if [[ $l > 2 ]]
        then
        echo "Too much args"
        _ugo_help
        return
    fi
    
    local project="$1"
    if [[ "$project" == "" ]]
        then
            _ugo_list
            return
    fi

    local ugo_project="$UGO_HOME/$project"
    if [ ! -d "$ugo_project" ]
        then
        echo "There is no such project: $project"
        return
    fi

    local ugo_profile="$ugo_project/$UGO_PROFILE"
    local project_dir
    if [[ -f "$ugo_profile" ]]
        then
        project_dir=$(cat "$ugo_profile")
    else
        echo "Strange error: No project-file: $ugo_profile"
        return
    fi

    local delete="$2"
    if [[ $delete != "" ]] && [[ $delete != "--all" ]]
        then
        echo "Wrong option: $delete"
        _ugo_help
        return
    fi

    if [[ "$project" == "$UGO_CONFDIR" ]]
        then
        echo "ugo conf directory $UGO_CONFDIR can´t be deleted."
        return
    fi
        
    local error_not_posible="Löschen nicht möglich. Der Papierkorb enthält das Projekt bereits. Bitte den Papierkorb vorher leeren"
    local dest="$UGO_TRASH/$project"
    local dest1 dest2
    local timestamp="`date +%s`"
    
    if [[ $delete == "--all" ]]
        then
        
        echo
        echo "ACHTUNG! Projekt-Ordner $project_dir wirklich in den Papierkorb verschieben? (Y/N)"
        read answer
        echo
        
        if [[ $answer == "Y" ]]
            then
            dest2=$dest"_projectdir_$timestamp"
            
            _ugo_run_hook $project 'pre-delete-hook'
            
            [[ $project == "$(pwd | awk '{print $9}' | xargs -n1 basename)" ]] && cd ..
            
            mv $project_dir $dest2
            
            if [[ $? == "0" ]]
                then
                echo "$project_dir nach $dest2 verschoben"
                echo
                _ugo_run_hook $project 'post-delete-hook'
            else
                echo $error_not_posible
            fi                    
        else
            echo "Abbruch. Projekt-Ordner $project_dir nicht gelöscht."
            echo
            return                        
        fi
    fi
    
    echo "ugo Projekt $ugo_project wirklich in den Papierkorb verschieben? (Y/N)"
    read answer
    echo
    
    if [[ $answer == "Y" ]]
        then
        dest1=$dest"_ugodir_$timestamp"
        mv $ugo_project $dest1
        if [[ $? == "0" ]]
            then 
            echo "$ugo_project nach $dest1 verschoben"
            echo
        else
            echo $error_not_posible
        fi
    else
        echo "Abbruch. ugo Projekt $ugo_project nicht gelöscht."
        echo
        return
    fi    
}

_ugo_info(){
    
    local l
    let l=${#@}
    if [[ $l > 1 ]]
        then
        echo "Too much args"
        _ugo_help
        return
    fi    
    
    local project=$1
    
    if [[ $project == "" ]]
        then 
        echo "ugo manages $(ugo | wc -l) projects"
        return
    fi
    
    local ugo_path="$UGO_HOME/$project"
    local ugo_profile="$ugo_path/$UGO_PROFILE"

    if [[ ! -f "$ugo_profile" ]]
        then
        echo "No projectfile: $ugo_profile."
        return
    fi
    
    local project_dir=$(cat "$ugo_profile")
    
    echo "Project settings: $project_dir"
}

_ugo_ugo(){
    
    local l
    local project=$1
    local ugo_path="$UGO_HOME/$project"
    local ugo_profile="$ugo_path/$UGO_PROFILE"
    local cmd=$2
    local cmd_option=$3

    if [[ ! -f "$ugo_profile" ]]
        then
        echo "No projectfile: $ugo_profile."
        return
    fi
    
    local project_dir=$(cat "$ugo_profile")
    
    case $cmd in
        "info")
            echo "Project settings: $project_dir"
            return
            ;;
        "conf")
            _ugo_conf $project
            return
            ;;
        "delete")
            _ugo_delete $project $cmd_option
            return
            ;;
        "set")
            _ugo_set $project $cmd_option
            return
            ;;
            
    esac
    
    if [[ ! -d "$project_dir" ]]
        then
        echo "Project Directory $project_dir does not exist."
        return
    fi
    
    _ugo_run_hook $project 'pre-ugo-hook'
    
    cd "$project_dir"
    
    _ugo_run_hook $project 'post-ugo-hook'
}

ugo(){


    local args=($(echo ${@:2}))
    
    if [[ ${!#} == "-v" ]]
        then
        UGO_DEBUG="1"
        #echo "DEBUG ON"
        unset args[${#args[@]}-1]
    else
        UGO_DEBUG="0"
        #echo "DEBUG OFF"
    fi
    
    args=${args[@]}
    
    local i
    local l
    local cmd="$1"

    if [ ! $cmd ]
        then
        _ugo_list
        return
    fi

    case "$cmd" in
        "-h")
            _ugo_help
            return;;
    esac

    for i in ${UGO_COMMANDS[@]}
    do
        if [[ $i == "$cmd" ]]
            then
            cmd="_ugo_$cmd $args"
            echo "<$cmd>"
            echo
            $cmd
            return
        fi
    done

    let l=${#@}
    if [[ $l > 2 ]]
        then
        echo "Inproper usage."
        echo
        _ugo_help
        return
    fi

    #default is ugo
    cmd="_ugo_ugo $cmd"
    [[ $args != "" ]] && cmd+=" $args"
    echo "<$cmd>"
    echo
    $cmd
}

_ugo_boot(){
    
    local answer
    
    local l
    let l=${#@}
    if [[ $l > 2 ]]
        then
        echo "Too much args"
        _ugo_help
        return
    fi
    
    local scriptname=$1
    if [[ $scriptname == "" ]]
        then
        echo "Kein Script angegeben"
        return
    fi
        
    local project=$2
    local cur_dir=$(pwd | sed 's/[ .]//g' | awk '{print $9}' | xargs -n1 basename)    
    if [[ $project == "" ]]
        then
        project=$cur_dir
    fi
    
    #problems with regex, so check for in array:(
    local projects=($(_ugo_list))
    local existing="0"
    local bla
    for bla in ${projects[@]}
    do
        [[ $bla == "$project" ]] && existing="1"
    done
    
    if [[ $existing == "0" ]]
        then

        if [[ "$project" != "$cur_dir" ]]
            then
            echo "Abbruch. Das Projekt gibt es nicht und es entspricht auch nicht dem aktuellen Verzeichnis."
            return
        fi
        
        echo "Projekt $project gibt es nicht als ugo-Projekt. Use make."
        echo "Trotzdem booten? (Y/N) - Angewendet auf aktuelles Verzeichnis: $cur_dir"
        read answer
        echo
        if [[ $answer != "Y" ]]
            then
            echo "Abbruch"
            return
        fi
    fi

    if [[ $scriptname =~ ^boot- ]]
        then
        
        local error_message    
        local cmd="_ugo_run_hook $UGO_CONFDIR $scriptname $project"
        
        if [[ "$project" != "$cur_dir" ]]
            then            
            ugo $project
            error_message="WARNING. Check settings. Possible project missmatch"
        else
            error_message="Boot finish"

        fi
        
        if [ "$(ls -A .)" ]
            then
            echo "ACHTUNG! Projekt-Verzeichnis ist nicht leer."
            echo "Trotzdem booten? (Y/N)"
            read answer
            echo
            if [[ $answer != "Y" ]]
                then
                echo "Abbruch"
                return
            fi
        fi

        $cmd

        echo
        echo $error_message
        echo        
        
    else
        echo "boot-filename has to start with boot-: $scriptname"
    fi    
}

# Run the hooks
_ugo_run_hook() {

    [[ ! -d $UGO_HOME/$UGO_CONFDIR ]] && echo "No confdir: '$UGO_CONFDIR'."

    local project=$1
    local scriptname=$2
    local ugo_path="$UGO_HOME/$project"
    local hook_script="$ugo_path/$scriptname"

    if [[ $project == "$UGO_CONFDIR" ]] && [[ $3 != "" ]]
        then
        project=$3
    fi

    if [ ! -f "$hook_script" ]
    then
        [[ $UGO_DEBUG == "1" ]] && echo "Hook script is missing: $hook_script."
    else
        echo "Hook: $hook_script"
        if [[ $UGO_DEBUG == "1" ]]
            then
            echo "Hook content:"
            cat "$hook_script"
            echo
        fi
        echo "Hook result:"
        echo
        source "$hook_script" $project        
    fi
    echo
}

#echo some header e.g. in bootscripts
_ugo_divider(){

 echo "------"
 echo "$1"
 echo "------" 
}

# Completion Section
_ugo()
{
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local prev="${COMP_WORDS[COMP_CWORD-1]}"
    local ugo_cmds="`echo ${UGO_COMMANDS[@]}`"
    
    local projects=$(_ugo_list)    
    local choices="$ugo_cmds $projects"
    local commands
    local p_list
    
    if [ $COMP_CWORD == 1 ]
        then
        COMPREPLY=($(compgen -W "$choices" -- ${cur}))
    fi
        
    if [ $COMP_CWORD == 2 ]
         then
         
         case "$prev" in
            "make") 
                p_list=$(pwd | sed 's/[ .]//g' | awk '{print $9}' | xargs -n1 basename)
                COMPREPLY=($(compgen -W "${p_list}" -- ${cur}))                
                return;;
            "list")
                projects+=" conf";;
            "conf")
                projects+=" list";;
            "boot")
                COMPREPLY=($(compgen -W "$(_ugo_list conf boot-)" -- ${cur}))
                return
                ;;
            "help")
                return
                ;;
                
         esac
         
         local i
         for i in $ugo_cmds
         do
             if [[ $i == "$prev" ]]
                 then
                 COMPREPLY=($(compgen -W "${projects}" -- ${cur}))
                 return
             fi
         done

         commands="conf info delete set"  
         COMPREPLY=($(compgen -W "${commands}" -- ${cur}))
     fi
      
     if [ $COMP_CWORD == 3 ]
        then
        local preprev="${COMP_WORDS[COMP_CWORD-2]}"
        case $preprev in
             "make")
                commands="boot"
                ;;
             "boot")
                commands=$(_ugo_list)
                ;;
                *)
                commands=""
                ;;
        esac
        
        [[ $commands != "" ]] && COMPREPLY=($(compgen -W "${commands}" -- ${cur}))         
     fi

     if [ $COMP_CWORD == 4 ]
         then   
         case "$prev" in
             "boot")
                 local p_list=$(_ugo_list conf boot-)
                 COMPREPLY=($(compgen -W "${p_list}" -- ${cur}))
                 ;;
         esac
     fi     
     
}
complete -o nospace -F _ugo ugo
