MODULE PythonCtrlR

    PERS jointtarget jTargetR := [[45.61,-116.06,43.58,-67.95,53.2,160.17],
                                  [-104.16,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11,5.15662E+11]];
    
    PERS robtarget pTargetR1 := [[170.504,-137.481,125.661],
                                 [0.657778,-0.74957,0.048605,0.055776],
                                 [1,-1,2,4],
                                 [-102.218,9E+09,9E+09,9E+09,9E+09,9E+09]];

    PERS num cmdR := 0;      ! 1=Execute MoveAbsJ
    PERS num cmdLinR := 0;   ! 1=Execute MoveL
    PERS num cmdGrip := 0;   ! 1=Ouvrir , 2=Fermer 

    PROC mainPyR()
        g_Init;
        WaitTime 2;
        WHILE TRUE DO
            ! Mouvement Articulaire
            IF cmdR = 1 THEN
                cmdR := 2;
                MoveAbsJ jTargetR\NoEOffs, v50, fine, tool0;
                cmdR := 0;
            ENDIF
            
            ! Mouvement Linéaire
            IF cmdLinR = 1 THEN
                cmdLinR := 2;
                MoveL pTargetR1, v50, fine, tool0;
                cmdLinR := 0;
            ENDIF
            
            ! Contrôle Pince avec g_GripIn / g_GripOut
            IF cmdGrip = 1 THEN
                cmdGrip := 3;   
                g_GripOut;       
                cmdGrip := 0;  
            ELSEIF cmdGrip = 2 THEN
                cmdGrip := 3;  
                g_GripIn;     
                cmdGrip := 0;   
            ENDIF
            
            WaitTime 0.05;
        ENDWHILE
 
    ENDPROC
ENDMODULE