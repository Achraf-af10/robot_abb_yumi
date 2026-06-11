MODULE PythonCtrlR
    PERS tooldata tPince3D := [TRUE,[[-0.430664,-0.747915,115.185],[1,0,0,0]],
                               [0.353,[7.4,2.5,22.1],[1,0,0,0],0,0,0]];

    PERS wobjdata wPlaque := [FALSE,TRUE,"",
                              [[230.965,117.998,10.254],[0.704838,-0.000574845,0.00201452,-0.709365]],
                              [[0,0,0],[1,0,0,0]]];
    PERS wobjdata zonePriseR := [FALSE,TRUE,"",
                                  [[462.39,31.05,63.03],[0.00294,-0.99873,-0.05036,0.00093]],
                                  [[0,0,0],[1,0,0,0]]];
    PERS wobjdata zonePoseR  := [FALSE,TRUE,"",
                                  [[319.17,33.56,83.98],[0.00292,-0.99873,-0.05035,0.00093]],
                                  [[0,0,0],[1,0,0,0]]];

    PERS robtarget pTargetR1  := [[0,0,0],[1,0,0,0],
                                   [-1,2,-1,4],[175.552,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget pPriseR    := [[-3.01,29.65,-100],[1,0,0,0],
                                   [1,-2,-2,4],[-139.106,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS robtarget pPoseR     := [[0,0,-100],[1,0,0,0],
                                   [1,-2,-2,4],[-139.106,9E+09,9E+09,9E+09,9E+09,9E+09]];
    PERS jointtarget jTargetR := [[113.3,-84.39,31.66,-138.56,115.91,-123.07],
                                   [-66.23,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11]];

    ! === POINT DE RENCONTRE ===
    ! Positionner le bras droit manuellement à la position de transfert
    ! puis remplacer ces valeurs par celles lues sur le FlexPendant
    CONST robtarget pMeetR := [[347.55,-87.21,219.76],[0.706869,-0.705093,-0.0156084,0.0541848],[1,-2,-1,5],[175.087,9E+09,9E+09,9E+09,9E+09,9E+09]];

    ! === SYNCHRONISATION ===
    VAR syncident syncPret;
    VAR syncident syncFerme;
    VAR syncident syncLache;
    PERS tasks tsklst{2} := [["T_ROB_L"],["T_ROB_R"]];

    ! === VARIABLES DE CONTRÔLE ===
    PERS num cmdR         := 0;
    PERS num cmdLinR      := 0;
    PERS num cmdGripR     := 0;
    PERS num dxR          := 0;
    PERS num dyR          := 0;
    PERS num dzR          := 0;
    PERS num cmdRelR      := 0;
    PERS num speedValR    := 50;
    PERS num cmdLinPriseR := 0;
    PERS num cmdLinPoseR  := 0;
    PERS num cmdRelPriseR := 0;
    PERS num cmdRelPoseR  := 0;
    
    PERS num cmdHandoverR2 := 0;  ! Donner la pièce à L

    PROC mainPyR()
        g_Init;
        WHILE TRUE DO
            ! MoveAbsJ
            IF cmdR = 1 THEN
                cmdR := 2;
                IF speedValR <= 10 THEN
                    MoveAbsJ jTargetR\NoEOffs, v10, z50, tPince3D;
                ELSEIF speedValR <= 50 THEN
                    MoveAbsJ jTargetR\NoEOffs, v50, z50, tPince3D;
                ELSE
                    MoveAbsJ jTargetR\NoEOffs, v100, z50, tPince3D;
                ENDIF
                cmdR := 0;
            ENDIF

            ! MoveL monde
            IF cmdLinR = 1 THEN
                cmdLinR := 2;
                ConfL \Off;
                IF speedValR <= 10 THEN
                    MoveL pTargetR1, v10, fine, tPince3D;
                ELSEIF speedValR <= 50 THEN
                    MoveL pTargetR1, v50, fine, tPince3D;
                ELSE
                    MoveL pTargetR1, v100, fine, tPince3D;
                ENDIF
                ConfL \On;
                cmdLinR := 0;
            ENDIF

            ! MoveL zonePriseR
            IF cmdLinPriseR = 1 THEN
                cmdLinPriseR := 2;
                ConfL \Off;
                IF speedValR <= 5 THEN
                    MoveL pPriseR, v5, fine, tPince3D \WObj:=zonePriseR;
                ELSEIF speedValR <= 10 THEN
                    MoveL pPriseR, v10, fine, tPince3D \WObj:=zonePriseR;
                ELSEIF speedValR <= 50 THEN
                    MoveL pPriseR, v50, fine, tPince3D \WObj:=zonePriseR;
                ELSE
                    MoveL pPriseR, v100, fine, tPince3D \WObj:=zonePriseR;
                ENDIF
                ConfL \On;
                cmdLinPriseR := 0;
            ENDIF

            ! MoveL zonePoseR
            IF cmdLinPoseR = 1 THEN
                cmdLinPoseR := 2;
                ConfL \Off;
                IF speedValR <= 10 THEN
                    MoveL pPoseR, v10, fine, tPince3D \WObj:=zonePoseR;
                ELSEIF speedValR <= 50 THEN
                    MoveL pPoseR, v50, fine, tPince3D \WObj:=zonePoseR;
                ELSE
                    MoveL pPoseR, v100, fine, tPince3D \WObj:=zonePoseR;
                ENDIF
                ConfL \On;
                cmdLinPoseR := 0;
            ENDIF

            ! MoveL relatif wPlaque
            IF cmdRelR = 1 THEN
                cmdRelR := 2;
                ConfL \Off;
                MoveL RelTool(CRobT(\Tool:=tPince3D \WObj:=wPlaque), dxR, dyR, dzR),
                      v50, fine, tPince3D \WObj:=wPlaque;
                ConfL \On;
                cmdRelR := 0;
            ENDIF

            ! MoveL relatif zonePriseR
            IF cmdRelPriseR = 1 THEN
                cmdRelPriseR := 2;
                ConfL \Off;
                MoveL RelTool(CRobT(\Tool:=tPince3D \WObj:=zonePriseR), dxR, dyR, dzR),
                      v50, fine, tPince3D \WObj:=zonePriseR;
                ConfL \On;
                cmdRelPriseR := 0;
            ENDIF

            ! MoveL relatif zonePoseR
            IF cmdRelPoseR = 1 THEN
                cmdRelPoseR := 2;
                ConfL \Off;
                MoveL RelTool(CRobT(\Tool:=tPince3D \WObj:=zonePoseR), dxR, dyR, dzR),
                      v50, fine, tPince3D \WObj:=zonePoseR;
                ConfL \On;
                cmdRelPoseR := 0;
            ENDIF

            ! Pince
            IF cmdGripR = 1 THEN cmdGripR := 3; g_GripOut; cmdGripR := 0;
            ELSEIF cmdGripR = 2 THEN cmdGripR := 3; g_GripIn; cmdGripR := 0;
            ENDIF

            ! Donner pièce à L
            IF cmdHandoverR2 = 1 THEN
                cmdHandoverR2 := 2;
                Handover_R2;
                cmdHandoverR2 := 0;
            ENDIF

            WaitTime 0.05;
        ENDWHILE
    ENDPROC

    PROC Handover_R2()
        ! 1. Aller au point de rencontre (avec la pièce)
        MoveJ pMeetR, v50, fine, tPince3D;

        ! 2. Attendre que L soit en position
        WaitSyncTask syncPret, tsklst;

        ! 3. Attendre que L ferme sa pince
        WaitSyncTask syncFerme, tsklst;

        ! 4. Lâcher la pièce
        g_GripOut;
        WaitTime 0.5;

        ! 5. Reculer
        MoveL Offs(pMeetR, 0, -30, 0), v30, fine, tPince3D;

        ! 6. Signaler fin
        WaitSyncTask syncLache, tsklst;
    ENDPROC

ENDMODULE