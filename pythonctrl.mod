MODULE PythonCtrl
    PERS tooldata tPince3D := [TRUE,[[-0.430664,-0.747915,115.185],[1,0,0,0]],
                               [0.353,[7.4,2.5,22.1],[1,0,0,0],0,0,0]];

    PERS wobjdata zonePriseL := [FALSE,TRUE,"",
                                  [[510.34,49.25,67.77],[0.010186,0.0282638,0.136999,0.026473]],
                                  [[0,0,0],[1,0,0,0]]];
    PERS wobjdata zonePoseL  := [FALSE,TRUE,"",
                                  [[376.86,34.82,88.73],[0.137124,-0.0217512,0.989929,0.0276431]],
                                  [[0,0,0],[1,0,0,0]]];

    PERS robtarget pTargetL1 := [[449.027,42.451,162.962],[0.11951,-0.110987,-0.985401,-0.048827],
                                  [-1,1,-1,4],[90.38,9E9,9E9,9E9,9E9,9E9]];
    PERS robtarget pPriseL   := [[0,0,0],[1,0,0,0],
                                  [-1,2,-1,4],[175.56,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget pPoseL    := [[-54.85,-64.1,-100],[1,0,0,0],
                                  [-1,2,-1,4],[175.56,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS jointtarget jTarget := [[-54.98,-73.65,15.08,186.68,-66.4,-116.93],
                                  [82.62,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11]];

    ! === POINT DE RENCONTRE ===
    ! Positionner le bras gauche manuellement à la position de transfert
    ! puis remplacer ces valeurs par celles lues sur le FlexPendant
    CONST robtarget pMeetL :=  [[336.37,-51.05,211.86],[0.0760314,0.0816971,0.724306,-0.680387],[-1,2,-1,5],[177.524,9E+09,9E+09,9E+09,9E+09,9E+09]];

    ! === SYNCHRONISATION ===
    VAR syncident syncPret;
    VAR syncident syncFerme;
    VAR syncident syncLache;
    PERS tasks tsklst{2} := [["T_ROB_L"],["T_ROB_R"]];
    
    PERS num cmdReceiveL := 0;  ! Recevoir la pièce de R

    ! === VARIABLES DE CONTRÔLE ===
    PERS num cmd          := 0;
    PERS num cmdLinL      := 0;
    PERS num cmdGripL     := 0;
    PERS num dx           := 0;
    PERS num dy           := 0;
    PERS num dz           := -50;
    PERS num cmdRel       := 0;
    PERS num speedVal     := 100;
    PERS num cmdLinPriseL := 0;
    PERS num cmdLinPoseL  := 0;
    PERS num cmdRelPriseL := 0;
    PERS num cmdRelPoseL  := 0;

    PROC mainPy()
        g_Init;
        WHILE TRUE DO
            ! MoveAbsJ
            IF cmd = 1 THEN
                cmd := 2;
                IF speedVal <= 10 THEN
                    MoveAbsJ jTarget\NoEOffs, v10, z50, tPince3D;
                ELSEIF speedVal <= 50 THEN
                    MoveAbsJ jTarget\NoEOffs, v50, z50, tPince3D;
                ELSE
                    MoveAbsJ jTarget\NoEOffs, v100, z50, tPince3D;
                ENDIF
                cmd := 0;
            ENDIF

            ! MoveL monde
            IF cmdLinL = 1 THEN
                cmdLinL := 2;
                MoveL pTargetL1, v50, fine, tPince3D;
                cmdLinL := 0;
            ENDIF

            ! MoveL zonePriseL
            IF cmdLinPriseL = 1 THEN
                cmdLinPriseL := 2;
                MoveL pPriseL, v50, fine, tPince3D;
                cmdLinPriseL := 0;
            ENDIF

            ! MoveL zonePoseL
            IF cmdLinPoseL = 1 THEN
                cmdLinPoseL := 2;
                MoveL pPoseL, v50, fine, tPince3D \WObj:=zonePoseL;
                cmdLinPoseL := 0;
            ENDIF

            ! MoveL relatif zonePriseL
            IF cmdRelPriseL = 1 THEN
                cmdRelPriseL := 2;
                MoveL Offs(CRobT(\Tool:=tPince3D \WObj:=zonePriseL), dx, dy, dz),
                      v50, fine, tPince3D \WObj:=zonePriseL;
                cmdRelPriseL := 0;
            ENDIF

            ! MoveL relatif zonePoseL
            IF cmdRelPoseL = 1 THEN
                cmdRelPoseL := 2;
                MoveL Offs(CRobT(\Tool:=tPince3D \WObj:=zonePoseL), dx, dy, dz),
                      v50, fine, tPince3D \WObj:=zonePoseL;
                cmdRelPoseL := 0;
            ENDIF

            ! Pince
            IF cmdGripL = 1 THEN cmdGripL := 3; g_GripOut; cmdGripL := 0;
            ELSEIF cmdGripL = 2 THEN cmdGripL := 3; g_GripIn; cmdGripL := 0;
            ENDIF


            
            ! Recevoir pièce de R
            IF cmdReceiveL = 1 THEN
                cmdReceiveL := 2;
                Receive_L;
                cmdReceiveL := 0;
            ENDIF

            WaitTime 0.05;
        ENDWHILE
    ENDPROC


    
    PROC Receive_L()
        ! 1. Ouvrir pince et aller au point de rencontre
        g_GripOut;
        MoveL Offs(pMeetL, 0, 50, 0), v30, fine, tPince3D;
        WaitTime 0.5;
        MoveJ pMeetL, v50, fine, tPince3D;

        ! 2. Signaler que L est en position
        WaitSyncTask syncPret, tsklst;

        ! 3. Descendre sur la pièce et fermer
        g_GripIn;
        WaitTime 0.5;

        ! 4. Signaler pince fermée
        WaitSyncTask syncFerme, tsklst;

        ! 5. Attendre que R lâche
        WaitSyncTask syncLache, tsklst;

        ! 6. Reculer avec la pièce
        MoveL Offs(pMeetL, 0, 30, 0), v20, fine, tPince3D;
    ENDPROC

ENDMODULE