def ugo_help(args):

    print """
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
        --global--
        $UGO_HOME/$UGO_CONFDIR/
         pre-make-hook
         post-make-hook
         pre-ugo-hook
         post-ugo-hook

        --per project--
        $UGO_HOME/<project>/
         pre-ugo-hook
         post-ugo-hook
         pre-delete-hook [only with delete --all]
         post-delete-hook [only with delete --all]

        bootscripts:
        $UGO_HOME/$UGO_CONFDIR/
         boot-<name>
"""
