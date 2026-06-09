MODULE MainModule
    LOCAL CONST string YuMi_App_Program_Version:="1.0.1";
    TASK PERS tooldata tPince3D:=[TRUE,[[-0.430664,-0.747915,115.185],[1,0,0,0]],[0.353,[7.4,2.5,22.1],[1,0,0,0],0,0,0]];
    !Do not edit or remove this line!
    TASK PERS wobjdata wGrid:=[FALSE,TRUE,"",[[517.556,-0.161064,-3.15329],[0.693013,-0.000940106,0.000863192,-0.720924]],[[0,0,0],[1,0,0,0]]];
    !Do not edit or remove this line!
    TASK PERS tooldata tPointe3D:=[TRUE,[[-0.614658,-0.47242,144.97],[1,0,0,0]],[0.355,[7.6,2.6,25.2],[1,0,0,0],0,0,0]];
    TASK PERS wobjdata wPlaque:=[FALSE,TRUE,"",[[230.965,117.998,10.254],[0.704838,-0.000574845,0.00201452,-0.709365]],[[0,0,0],[1,0,0,0]]];
    ! ROBTARGET
    CONST robtarget Pprise:=[[-30,40,26],[0.000792493,-0.620605,0.784122,0.000913586],[-1,2,0,5],[120.533,9E+09,9E+09,9E+09,9E+09,9E+09]];

    !test
    VAR num x:=0;
    VAR num y:=0;
    VAR num z:=26;
    VAR num a:=80;
    VAR pos Pp;
    VAR pos Pd;
    !VAR robtarget PpriseL:=[[-30,40,33],[0.000613445,-0.502387,0.864642,0.00100369],[-1,2,0,5],[126.922,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget PpriseL;
    CONST robtarget pHome:=[[0,0,100],[0.000792493,-0.620605,0.784122,0.000913586],[-1,2,0,5],[120.533,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget pDepot;
    VAR robtarget pDepotC;
    CONST robtarget pHome20:=[[0.00,0.00,100.00],[0.000785064,-0.620598,0.784128,0.00091045],[-1,2,0,5],[120.533,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pHome10:=[[0.00,0.00,100.00],[0.000785064,-0.620598,0.784128,0.00091045],[-1,2,0,5],[120.533,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pInit:=[[-134.97,149.90,240.92],[0.5949,-0.53345,-0.259554,-0.542362],[-1,0,0,4],[113.145,9E+09,9E+09,9E+09,9E+09,9E+09]];

    VAR num CasePriseL{5}:=[0,0,0,0,0];
    VAR num CaseDepotL{5}:=[0,0,0,0,0];
    VAR bool FlagRANGE:=FALSE;

    ! Matrice de la situation du jeu
    PERS num MatriceJeu{2,5}:=[[0,5,0,4,2],[0,6,0,8,0]];
    ! compteur PERS des coups
    PERS num NombreCoup:=6;
    ! qui jou ? BLACK:FALSE / WHITE:TRUE
    PERS bool WhosPlayingNow:=FALSE;
    ! Game finish
    PERS bool GameFinish:=TRUE;
    !Position de synchronisation
    VAR syncident syncStep1;
    PERS tasks tsklstYUMI{2}:=[["T_ROB_R"],["T_ROB_L"]];
    ! Winner
    PERS string Winner{3}:=["Black","White","NULL"];
    ! IP and Port
    !VAR string IP:="10.2.30.125";
    VAR string IP:="10.2.30.128";
    VAR num PORT:=21;
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    VAR string text;
    VAR iodev infile;
    VAR socketdev socket1;
    VAR string str_data;
    ! Matrice de la situation du jeu
    VAR num MoveIA:=0;
    TASK PERS tooldata toolPointe3D:=[TRUE,[[-1.82406,-0.590086,147.244],[1,0,0,0]],[0.34,[7.2,2.6,25.2],[1,0,0,0],0,0,0]];
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    VAR syncident sync2;
    VAR syncident sync3;
    VAR syncident sync4;
    VAR syncident sync5;
    VAR syncident sync6;
    VAR syncident sync7;
    VAR syncident sync8;
    VAR syncident sync9;
    VAR syncident sync01;
    VAR syncident sync02;
    VAR syncident sync03;
    VAR syncident sync04;
    VAR syncident sync05;
    VAR syncident sync06;
    VAR syncident sync07;
    VAR syncident sync08;
    VAR syncident sync09;
    VAR syncident sync10;
    VAR syncident sync11;
    VAR syncident sync12;
    VAR syncident sync13;
    VAR syncident sync14;
    CONST robtarget pMeet:=[[113.73,153.66,194.81],[0.500441,-0.502386,0.496493,-0.500662],[-1,0,0,4],[152.637,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pMeet10:=[[132.25,153.88,194.49],[0.500536,-0.50265,0.496295,-0.500498],[-1,0,0,4],[152.601,9E+09,9E+09,9E+09,9E+09,9E+09]];

    VAR num CaseS:=19;
    PERS num Inc;
    Var num IncL;

    PROC main()
        !VAR num MatriceR{2,5}:=[[0,0,0,0,0],[0,0,0,0,0]];
        !VAR num compC:=0;

        !T_Init_L;
        !****************************************************
        ! RANGEMENT
        !MatriceR:=MatriceJeu;
        IncL:=15;
        WaitSyncTask sync01,tsklstYUMI;
        
        FlagRANGE:=TRUE;
        !T_Init_L;
        T_RANGEV1_L;
        WaitSyncTask sync02,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=3 THEN
                T_ECHANGE_L 0,IncL;
                IncL:=IncL+1;
            ENDIF
        ENDFOR
        WaitSyncTask sync03,tsklstYUMI;

        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=6 THEN
                T_ECHANGE_L 0,IncL;
                IncL:=IncL+1;
                !T_ECHANGE_L 0,(19-Inc);
            ENDIF
        ENDFOR
        WaitSyncTask sync04,tsklstYUMI;
        !T_ECHANGE_L 0,(19-Inc);

        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=9 THEN
                T_ECHANGE_L 0,IncL;
                IncL:=IncL+1;
            ENDIF
        ENDFOR
        WaitSyncTask sync05,tsklstYUMI;
        !===============================================
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=1 THEN
                T_ECHANGE_L 1,0;
                MatriceJeu{2,i}:=0;
            ENDIF
        ENDFOR
        WaitSyncTask sync06,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=4 THEN
                T_ECHANGE_L 4,0;
                MatriceJeu{2,i}:=0;
            ENDIF
        ENDFOR
        WaitSyncTask sync07,tsklstYUMI;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=7 THEN
                T_ECHANGE_L 7,0;
                MatriceJeu{2,i}:=0;
                !IncL:=IncL-1;
            ENDIF
        ENDFOR

        !****************************************************
        Reset Collision_Avoidance;
        ! Rangement milieu
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=2 THEN
                T_MovePtoCase 2,IncL;
                IncL:=IncL+1;
            ENDIF
        ENDFOR
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=5 THEN
                T_MovePtoCase 5,IncL;
                IncL:=IncL+1;
            ENDIF
        ENDFOR
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=8 THEN
                T_MovePtoCase 8,IncL;
                IncL:=IncL+1;
            ENDIF
        ENDFOR
        WaitSyncTask sync08,tsklstYUMI;


        T_Init_L;
        WaitSyncTask sync5,tsklstYUMI;
        !stop;
        !****************************************************
    ENDPROC

    PROC T_MovePtoCase(num nCaseP,num nCaseD)
        Pp:=CalcP(nCaseP);
        Pd:=CalcP(nCaseD);
        PpriseL:=[[Pp.x,Pp.y,26],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
        pDepot:=[[Pd.x,Pd.y,33],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
        pDepotC:=[[(Pd.x)/2,(Pd.y)/2,80],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
        !PRISE  
        !g_MoveTo 12.5\NoWait;
        g_MoveTo 12.5;
        !g_MoveTo 12.5;
        MoveJ RelTool(PpriseL,0,0,-150),v1500,z100,tPince3D\WObj:=wPlaque;
        MoveJ PpriseL,v1500,fine,tPince3D\WObj:=wPlaque;
        g_GripIn;
        MoveL RelTool(PpriseL,0,0,-80),v1500,fine,tPince3D\WObj:=wPlaque;
        ! DEPOT
        MoveJ RelTool(pDepot,0,0,-100),v1500,z100,tPince3D\WObj:=wPlaque;
        MoveL pDepot,v30,fine,tPince3D\WObj:=wPlaque;
        !g_GripOut \targetPos:=12;
        !g_MoveTo 12.5;
        !g_MoveTo 12.5\NoWait;
        g_MoveTo 12.5;
        MoveL RelTool(pDepot,0,0,-100),v1500,fine,tPince3D\WObj:=wPlaque;
    ERROR
        IF ERRNO=ERR_COLL_STOP THEN
            ! Current movement on motion base path level
            ! is already stopped.
            ! New motion path level for new movements in the ERROR handler
            !StorePath;
            RestoPath;
            StartMove;
            !RestoPath;
            ! Restart the stopped movements on motion base path level,
            ! restart the process and retry program execution
            !StartMoveRetry;
        ENDIF

    ENDPROC

    PROC RANGEL()
        VAR num CaseDepotTemp{5}:=[19,18,17,16,15];
        VAR bool isLeftHandCalibrated;

        ! FlagRange
        FlagRANGE:=TRUE;
        !!!! Check and Calibrate the hand 
        isLeftHandCalibrated:=g_IsCalibrated();
        IF isLeftHandCalibrated=FALSE THEN
            g_init;
            g_Calibrate\Jog;
        ENDIF

        LecturePos;
        FOR i FROM 1 TO 5 DO
            IF CaseDepotL{i}<>0 THEN
                T_MovePtoCase CaseDepotL{i},CaseDepotTemp{i};
            ENDIF

        ENDFOR
        FlagRANGE:=FALSE;
    ENDPROC

    FUNC pos CalcP(num CaseP)
        VAR pos P;
        TEST CaseP
        CASE 1:
            x:=a/2;
            y:=(5*a)/2;
        CASE 2:
            x:=(3*a)/2;
            y:=(5*a)/2;
        CASE 3:
            x:=(5*a)/2;
            y:=(5*a)/2;
        CASE 4:
            x:=(a)/2;
            y:=(3*a)/2;
        CASE 5:
            x:=(3*a)/2;
            y:=(3*a)/2;
        CASE 6:
            x:=(5*a)/2;
            y:=(3*a)/2;
        CASE 7:
            x:=(a)/2;
            y:=(a)/2;
        CASE 8:
            x:=(3*a)/2;
            y:=(a)/2;
        CASE 9:
            x:=(5*a)/2;
            y:=(a)/2;
        CASE 10:
            x:=((5*a)/2)+70;
            y:=(a)/2;
        CASE 11:
            x:=(5*a)/2+70;
            y:=((a)/2)+40;
        CASE 12:
            x:=(5*a)/2+70;
            y:=((a)/2)+(2*40);
        CASE 13:
            x:=(5*a)/2+70;
            y:=((a)/2)+(3*40);
        CASE 14:
            x:=(5*a)/2+70;
            y:=((a)/2)+(4*40);
        CASE 15:
            x:=-30;
            y:=5*a/2;
        CASE 16:
            x:=-30;
            y:=4*a/2;
        CASE 17:
            x:=-30;
            y:=3*a/2;
        CASE 18:
            x:=-30;
            y:=2*a/2;
        CASE 19:
            x:=-30;
            y:=a/2;
            !DEFAULT:
            !x:=(a)/2;
            !y:=(a)/2;
        ENDTEST
        P.x:=x;
        P.y:=y;
        P.z:=0;
        RETURN P;
    ENDFUNC

    PROC LecturePos()
        FOR i FROM 1 TO 5 DO
            CaseDepotL{i}:=MatriceJeu{1,i};
        ENDFOR
    ENDPROC

    PROC T_Init_L()
        MoveJ [[-100.68,138.05,196.28],[0.643705,-0.744762,0.168569,-0.0505757],[-1,0,1,4],[120.224,9E+09,9E+09,9E+09,9E+09,9E+09]], v100, z50, tPince3D\WObj:=wPlaque;
        MoveJ [[-47.87,-162.91,128.99],[0.46482,-0.8718,-0.0146111,-0.153925],[0,0,1,4],[103.678,9E+09,9E+09,9E+09,9E+09,9E+09]],v100,z50,tPince3D\WObj:=wPlaque;
    ENDPROC

    PROC T_MEET_L()
        MoveJ RelTool(pMeet,0,0,-100)\ID:=70,v1500,z100,tPince3D\WObj:=wPlaque;
        MoveJ pMeet\ID:=71,v300,z100,tPince3D\WObj:=wPlaque;
    ENDPROC

    PROC T_PRISE_L(num nCaseP)
        Pp:=CalcP(nCaseP);
        PpriseL:=[[Pp.x,Pp.y,26],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
        !PRISE  
        g_MoveTo 12.5;
        !g_MoveTo 12.5\NoWait;
        MoveJ RelTool(PpriseL,0,0,-150),v1500,z100,tPince3D\WObj:=wPlaque;
        MoveJ PpriseL,v1500,fine,tPince3D\WObj:=wPlaque;
        g_GripIn;

        MoveL RelTool(PpriseL,0,0,-80),v1500,fine,tPince3D\WObj:=wPlaque;

    ENDPROC

    PROC T_DEPOT_L(num nCaseD)
        Pd:=CalcP(nCaseD);
        pDepot:=[[(Pd.x-0.9),(Pd.y),24],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
        ! DEPOT
        MoveJ RelTool(pDepot,0,0,-100),v1500,z100,tPince3D\WObj:=wPlaque;
        MoveL pDepot,v30,fine,tPince3D\WObj:=wPlaque;
        !g_MoveTo 12.5\NoWait;
        g_MoveTo 12.5;
        MoveL RelTool(pDepot,0,0,-100),v1500,fine,tPince3D\WObj:=wPlaque;
    ENDPROC

    PROC T_ECHANGE_L(num nCaseP,num nCaseD)
        IF nCaseP<>0 THEN
            T_PRISE_L nCaseP;
            SyncMoveOn sync2,tsklstYUMI;
            T_MEET_L;
            SyncMoveOff sync2;
            MoveL pMeet10,v100,z150,tPince3D\WObj:=wPlaque;
            !v30
            WaitSyncTask sync3,tsklstYUMI;
            WaitSyncTask sync4,tsklstYUMI;
            !g_GripOut;
            g_MoveTo 12.5;
            !g_MoveTo 12.5\NoWait;
            MoveJ RelTool(pMeet,0,0,-100),v100,z100,tPince3D\WObj:=wPlaque;
        ELSEIF nCaseD<>0 THEN
            !g_GripOut;
            g_MoveTo 12.5\NoWait;
            SyncMoveOn sync2,tsklstYUMI;
            T_MEET_L;
            SyncMoveOff sync2;
            WaitSyncTask sync3,tsklstYUMI;
            g_GripIN;
            WaitSyncTask sync4,tsklstYUMI;
            MoveJ RelTool(pMeet,0,0,-100),v100,z150,tPince3D\WObj:=wPlaque;
            T_DEPOT_L nCaseD;
        ENDIF
    ENDPROC


    PROC T_RANGEV1_L()
        VAR bool isLeftHandCalibrated;
        ! FlagRange
        FlagRANGE:=TRUE;
        !!!! Check and Calibrate the hand 
        isLeftHandCalibrated:=g_IsCalibrated();
        IF isLeftHandCalibrated=FALSE THEN
            g_init;
            g_Calibrate\Jog;
        ENDIF

        LecturePos;
        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{1,i}=7 THEN
                T_MovePtoCase CaseDepotL{i},IncL;
                IncL:=IncL+1;
            ENDIF
            IF MatriceJeu{1,i}=4 THEN
                T_MovePtoCase CaseDepotL{i},IncL;
                IncL:=IncL+1;
            ENDIF
            IF MatriceJeu{1,i}=1 THEN
                T_MovePtoCase CaseDepotL{i},IncL;
                IncL:=IncL+1;
            ENDIF
        ENDFOR
        FlagRANGE:=FALSE;


    ENDPROC

ENDMODULE