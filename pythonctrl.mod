MODULE PythonCtrl

    PERS jointtarget jTarget := [[-43.57,-123.11,41.18,69.03,55.85,28.89],[105.12,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11]];
    PERS robtarget pTargetL1 := [[159.579,132.171,230.892],[0.013482,0.040235,-0.739789,0.671499],[0,1,0,4],[107.618,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    PERS num cmd := 0;      ! 1=Execute MoveAbsJ
    PERS num cmdLinL := 0;  ! 1=Execute MoveL
    PERS num cmdGripL := 0; ! 1=Ouvrir, 2=Fermer

    PROC mainPy()
        g_Init;
        WaitTime 2;
        WHILE TRUE DO
            ! Mouvement Articulaire
            IF cmd = 1 THEN
                cmd := 2;
                MoveAbsJ jTarget\NoEOffs, v50, fine, tool0;
                cmd := 0;
            ENDIF
            
            ! Mouvement Linéaire
            IF cmdLinL = 1 THEN
                cmdLinL := 2;
                MoveL pTargetL1, v50, fine, tool0;
                cmdLinL := 0;
            ENDIF
            
            ! Contrôle Pince avec g_GripIn / g_GripOut

            IF cmdGripL = 1 THEN
                cmdGripL := 3;   
                g_GripOut;         
                cmdGripL := 0;     
            ELSEIF cmdGripL = 2 THEN
                cmdGripL := 3;     
                g_GripIn;          
                cmdGripL := 0;    
            ENDIF
            
            WaitTime 0.05;
        ENDWHILE

    ENDPROC
ENDMODULE