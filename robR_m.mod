
MODULE Mouvement
    CONST robtarget PpriseVue:=[[120.18,123.77,365.95],[0.00607128,0.713107,0.700988,0.00761596],[1,1,1,4],[172.522,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS wobjdata wCamera:=[FALSE,TRUE,"",[[355.092,26.4199,7.9322],[0.704275,-0.00110283,-0.000172004,-0.709926]],[[0,0,0],[1,0,0,0]]];

    ! ROBTARGET
    CONST robtarget Pprise:=[[-30,40,26],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget myRobtarget:=[[100,200,300],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR bool FlagRANGE:=FALSE;

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
    CONST robtarget pHome20:=[[0.00,0.00,100.00],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pHome10:=[[0.00,0.00,100.00],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pInit:=[[381.95,172.31,192.09],[0.66085,-0.745614,0.0388022,0.0763645],[1,0,1,4],[-104.986,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR robtarget pMeet10:=[[140,153.34,195.98],[0.490246,-0.50676,-0.494201,0.508546],[1,0,2,4],[-150.587,9E+09,9E+09,9E+09,9E+09,9E+09]];
    !VAR robtarget pMeet10:=[[132.25,153.34,195.98],[0.490246,-0.50676,-0.494201,0.508546],[1,0,2,4],[-150.587,9E+09,9E+09,9E+09,9E+09,9E+09]];

    CONST robtarget pMeet:=[[158.89,153.25,196.06],[0.489972,-0.506662,-0.494454,0.50866],[1,0,2,4],[-150.61,9E+09,9E+09,9E+09,9E+09,9E+09]];
    VAR num CaseS:=10;
    CONST robtarget PpriseVue10:=[[114.03,126.20,357.79],[0.0060667,0.713118,0.700977,0.00761506],[1,1,1,4],[172.526,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget PpriseVue20:=[[113.83,124.56,362.97],[0.0060662,0.713117,0.700977,0.00761729],[1,1,1,4],[172.531,9E+09,9E+09,9E+09,9E+09,9E+09]];


    PROC T_MovePtoCase(num nCaseP,num nCaseD)
        IF nCaseP<>0 AND nCaseD<>0 THEN
            Pp:=CalcP(nCaseP);
            Pd:=CalcP(nCaseD);
            PpriseL:=[[Pp.x,Pp.y,26],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
            pDepot:=[[Pd.x,Pd.y,30],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
            !PRISE  
            !g_MoveTo 12.5\NoWait;
             g_MoveTo 12.5;
            MoveJ RelTool(PpriseL,0,0,-150),v1500,z100,tPince3D\WObj:=wPlaque;
            MoveJ PpriseL,v1500,fine,tPince3D\WObj:=wPlaque;
            g_GripIn;
            MoveL RelTool(PpriseL,0,0,-80),v1500,fine,tPince3D\WObj:=wPlaque;
            ! DEPOT
            MoveJ RelTool(pDepot,0,0,-80),v1500,z100,tPince3D\WObj:=wPlaque;
            MoveL pDepot,v30,fine,tPince3D\WObj:=wPlaque;
            !g_GripOut \targetPos:=12;
            !g_MoveTo 12.5\NoWait;
             g_MoveTo 12.5;
            MoveL RelTool(pDepot,0,0,-100),v1500,fine,tPince3D\WObj:=wPlaque;
            IF FlagRANGE=FALSE THEN
                T_PriseVue;
            ENDIF
        ENDIF
    ERROR
        IF ERRNO=ERR_COLL_STOP THEN
            ! Current movement on motion base path level
            ! is already stopped.
            ! New motion path level for new movements in the ERROR handler
            !StorePath; 
            RestoPath;
            StartMove;

            ! Restart the stopped movements on motion base path level,
            ! restart the process and retry program execution
            !StartMoveRetry;
        ENDIF

    ENDPROC

    PROC RANGE(num CasePrise{*},num CaseDepot{*})
        FlagRANGE:=TRUE;
        FOR i FROM 1 TO 5 DO
            T_MovePtoCase CaseDepot{i},CasePrise{i};
        ENDFOR
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

    PROC T_PriseVue()
        MoveJ PpriseVue,v1000,z50,VisionR\WObj:=wPlaque;
        !MoveJ PpriseVue10, v1000, z50, VisionR\WObj:=wPlaque;
        !MoveJ PpriseVue20, v1000, z50, VisionR\WObj:=wPlaque;
    ENDPROC

    PROC T_Init()
        MoveJ [[330.96,87.05,148.99],[0.054479,0.964933,0.252445,-0.0469786],[1,0,1,4],[-138.031,9E+09,9E+09,9E+09,9E+09,9E+09]], v100, z50, VisionR\WObj:=wPlaque;
        MoveJ [[274.26,-155.12,144.49],[0.499918,-0.853266,-0.121152,0.085685],[0,0,1,4],[-105.643,9E+09,9E+09,9E+09,9E+09,9E+09]],v100,z50,tPince3D\WObj:=wPlaque;
    ENDPROC


    PROC T_MEET_R()
        MoveJ RelTool(pMeet,0,0,-100)\ID:=70,v1500,z100,tPince3D\WObj:=wPlaque;
        MoveJ pMeet\ID:=71,v300,z100,tPince3D\WObj:=wPlaque;
    ENDPROC


    PROC T_PRISE_R(num nCaseP)
        IF nCaseP<>0 THEN
            Pp:=CalcP(nCaseP);
            PpriseL:=[[Pp.x,Pp.y,24],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
            !PRISE  
            !g_MoveTo 12.5\NoWait;
            g_MoveTo 12.5;
            MoveJ RelTool(PpriseL,0,0,-150),v1500,fine,tPince3D\WObj:=wPlaque;
            MoveJ PpriseL,v1500,fine,tPince3D\WObj:=wPlaque;
            g_GripIn;
            MoveL RelTool(PpriseL,0,0,-80),v1500,fine,tPince3D\WObj:=wPlaque;
        ENDIF
    ENDPROC


    PROC T_DEPOT_R(num nCaseD)
        IF nCaseD<>0 THEN
            Pd:=CalcP(nCaseD);
            pDepot:=[[(Pd.x-0.7),Pd.y,24],[0.00269825,-0.704744,-0.709457,-8.30426E-05],[1,0,1,5],[-170.445,9E+09,9E+09,9E+09,9E+09,9E+09]];
            ! DEPOT
            MoveJ RelTool(pDepot,0,0,-80),v1500,z100,tPince3D\WObj:=wPlaque;
            MoveL pDepot,v30,fine,tPince3D\WObj:=wPlaque;
            !g_MoveTo 12.5\NoWait;
            g_MoveTo 12.5;
            MoveL RelTool(pDepot,0,0,-100),v1500,fine,tPince3D\WObj:=wPlaque;
            !MoveL Offs(RelTool(pDepot,0,0,-100),,),v1500,fine,tPince3D\WObj:=wPlaque;
        ENDIF
    ENDPROC

    PROC T_ECHANGE_R(num nCaseP,num nCaseD)
        IF nCaseP<>0 THEN
            T_PRISE_R nCaseP;
            SyncMoveOn sync2,tsklstYUMI;
            T_MEET_R;
            SyncMoveOff sync2;
            MoveL pMeet10,v100,z150,tPince3D\WObj:=wPlaque;
            !v30
            WaitSyncTask sync3,tsklstYUMI;
            WaitSyncTask sync4,tsklstYUMI;
            !g_GripOut;
            !g_MoveTo 12.5\NoWait;
            g_MoveTo 12.5;
            MoveJ RelTool(pMeet,0,0,-100),v100,z100,tPince3D\WObj:=wPlaque;
        ELSEIF nCaseD<>0 THEN
            !g_GripOut;
            !g_MoveTo 12.5\NoWait;
            g_MoveTo 12.5;
            SyncMoveOn sync2,tsklstYUMI;
            T_MEET_R;
            SyncMoveOff sync2;
            WaitSyncTask sync3,tsklstYUMI;
            g_GripIN;
            WaitSyncTask sync4,tsklstYUMI;
            MoveJ RelTool(pMeet,0,0,-100),v100,z150,tPince3D\WObj:=wPlaque;
            !v50
            T_DEPOT_R nCaseD;
        ENDIF
    ENDPROC


    PROC T_RANGEV1_R()

        FOR i FROM 1 TO 5 DO
            IF MatriceJeu{2,i}=9 THEN
                !T_MovePtoCase MatriceJeu{2,i}, CaseS;
                T_MovePtoCase MatriceJeu{2,i},IncR2;
                !CaseS:=CaseS+1;
                IncR2:=IncR2-1;
            ENDIF
            IF MatriceJeu{2,i}=6 THEN
                T_MovePtoCase MatriceJeu{2,i},IncR2;
                !CaseS:=CaseS+1;
                Inc:=Inc+1;
                IncR2:=IncR2-1;
            ENDIF
            IF MatriceJeu{2,i}=3 THEN
                T_MovePtoCase MatriceJeu{2,i},IncR2;
                !CaseS:=CaseS+1;
                Inc:=Inc+1;
                IncR2:=IncR2-1;
            ENDIF
        ENDFOR
    ENDPROC
ENDMODULE