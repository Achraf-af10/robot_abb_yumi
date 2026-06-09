MODULE PythonCtrl
    PERS jointtarget jTarget := [[-99.58,-61.43,13.96,115.53,84.61,-50.12],[90.38,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11]];
    PERS robtarget pTargetL1 := [[449.027,42.451,162.962],[0.11951,-0.110987,-0.985401,-0.048827],[-1,1,-1,4],[90.38,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    PERS num cmd := 0;      ! 1=Execute MoveAbsJ
    PERS num cmdLinL := 0;  ! 1=Execute MoveL
    PERS num cmdGripL := 0; ! 1=Ouvrir, 2=Fermer

    ! Variables pour mouvement relatif
    PERS num dx := 0;
    PERS num dy := 0;
    PERS num dz := 0;
    PERS num cmdRel := 0;   ! 1=Execute MoveL Relatif
    
    PERS num speedVal := 50;

    PROC mainPy()
        g_Init;
        WaitTime 2;
        WHILE TRUE DO
            ! Mouvement Articulaire
            IF cmd = 1 THEN
                cmd := 2;
                IF speedVal <= 10 THEN
                    MoveAbsJ jTarget\NoEOffs, v10, fine, tool0;
                ELSEIF speedVal <= 20 THEN
                    MoveAbsJ jTarget\NoEOffs, v20, fine, tool0;
                ELSEIF speedVal <= 50 THEN
                    MoveAbsJ jTarget\NoEOffs, v50, fine, tool0;
                ELSEIF speedVal <= 100 THEN
                    MoveAbsJ jTarget\NoEOffs, v100, fine, tool0;
                ELSEIF speedVal <= 200 THEN
                    MoveAbsJ jTarget\NoEOffs, v200, fine, tool0;
                ELSE
                    MoveAbsJ jTarget\NoEOffs, v500, fine, tool0;
                ENDIF
                cmd := 0;
            ENDIF
            
            ! Mouvement Linéaire Standard
            IF cmdLinL = 1 THEN
                cmdLinL := 2;
                ConfL \Off;
                MoveL pTargetL1, v50, fine, tool0;
                ConfL \On;
                cmdLinL := 0;
            ENDIF
            
            ! Mouvement Linéaire Relatif
            IF cmdRel = 1 THEN
                cmdRel := 2;
                ConfL \Off;
                MoveL RelTool(CRobT(), dx, dy, dz), v50, fine, GripperL;
                ConfL \On;
                cmdRel := 0;
            ENDIF
            
            ! Contrôle Pince
            IF cmdGripL = 1 THEN
                cmdGripL := 3; g_GripOut; cmdGripL := 0;
            ELSEIF cmdGripL = 2 THEN
                cmdGripL := 3; g_GripIn; cmdGripL := 0;
            ENDIF
            
            WaitTime 0.05;
        ENDWHILE
    ENDPROC
ENDMODULE