%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1

int yylex();
int yyerror();
%}

%token STRING;
%token NUMBER;
%token IF;
%token PRINT;
%token READINT;
%token READSTRING;
%token ELSE;
%token WHILE;
%token FOR;
%token IN;

%token IDENTIFIER;
%token STRINGCONSTANT;

%token PLUS;
%token MINUS;
%token TIMES;
%token DIV;
%token EQ;
%token BIGGER;
%token BIGGEREQ;
%token LESS;
%token LESSEQ;
%token EQQ;
%token NEQ;
%token PLUSEQ;
%token MINUSEQ;
%token TIMESEQ;
%token DIVEQ; 

%token SEMICOLON;
%token OPEN;
%token CLOSE;
%token BRACKETOPEN;
%token BRACKETCLOSE;
%token ARROPEN;
%token ARRCLOSE;
%token COMMA;

%start Program 

%%

Program : Stmt {printf("Program -> Stmt \n");} | 
          Stmt Program {printf("Program -> Stmt Program \n");}
Stmt : VarDeclStmt SEMICOLON {printf("Stmt -> VarDeclStmt ; \n");} |
       AssignStmt SEMICOLON {printf("Stmt -> AssignStmt ; \n");} | 
       StructStmt {printf("Stmt -> StructStmt SEMICOLON \n");}| 
       IOStmt SEMICOLON {printf("Stmt -> IOStmt ; \n");}
StructStmt : IfStmt {printf("StructStmt -> IfStmt \n");}| 
             ForStmt {printf("StructStmt -> ForStmt \n");}| 
             WhileStmt {printf("StructStmt -> WhileStmt \n");}

StmtList : Stmt {printf("StmtList -> Stmt \n");}| 
           Stmt StmtList {printf("StmtList -> Stmt Stmtlist \n");}
StmtBlock : BRACKETOPEN StmtList BRACKETCLOSE {printf("StmtBlock -> { StmtList } \n");} | 
            Stmt {printf("StmtBlock -> Stmt \n");}

IfStmt : IF OPEN Condition CLOSE StmtBlock {printf("IfStmt -> IF ( Condition ) StmtBlock \n");}|  
         IF OPEN Condition CLOSE StmtBlock ELSE StmtBlock {printf("IfStmt -> IF ( Condition ) StmtBlock ELSE StmtBlock \n");}
WhileStmt : WHILE OPEN Condition CLOSE StmtBlock {printf("WhileStmt -> WHILE ( Condition ) StmtBlock \n");}
ForStmt : FOR OPEN IDENTIFIER IN IDENTIFIER CLOSE StmtBlock {printf("ForStmt -> FOR ( IDENTIFIER IN IDENTIFIER ) StmtBlock \n");}
IOStmt : READINT OPEN CLOSE {printf("IOStmt -> READINT () \n");}|
         READSTRING OPEN CLOSE {printf("IOStmt -> READSTRING () \n");}| 
         PRINT OPEN STRINGCONSTANT CLOSE {printf("IOStmt -> PRINT ( STRINGCONSTANT ) \n");}| 
         PRINT OPEN IDENTIFIER CLOSE {printf("IOStmt -> PRINT ( IDENTIFIER ) \n");}

PrimitiveType : NUMBER {printf("PrimitiveType -> number \n");} | 
                STRING {printf("PrimitiveType -> string \n");} 
ArrayType : PrimitiveType ARROPEN ARRCLOSE {printf("ArrayType -> [] \n");} | 
            PrimitiveType ARROPEN NUMBER ARRCLOSE {printf("PrimitiveType -> [ number ] \n");} 
Type : PrimitiveType {printf("Type -> PrimitiveType \n");}| 
       ArrayType {printf("Type -> ArrayType \n");}

Expression : Expression PLUS Term | Expression MINUS Term  | Term | ArrayValue
Term : Term TIMES Factor | Term DIV Factor | Factor
Factor : OPEN Expression CLOSE | IDENTIFIER | NUMBER | READINT OPEN CLOSE {printf("IOStmt -> READINT () \n");}
ArrayValue : IDENTIFIER ARROPEN NUMBER ARRCLOSE

ArrayValues : Expression | Expression COMMA ArrayValues
ArrayConstant : ARROPEN ArrayValues ARRCLOSE

AssignOperator : EQ {printf("AssignOperator -> = \n");} | 
                 PLUSEQ {printf("AssignOperator -> += \n");}| 
                 MINUSEQ {printf("AssignOperator -> -= \n");}| 
                 TIMESEQ {printf("AssignOperator -> *= \n");}| 
                 DIVEQ {printf("AssignOperator -> /= \n");}
AssignStmt : IDENTIFIER AssignOperator Expression {printf("AssignStmt -> IDENTIFIER AssignOperator Expression \n");} 

VarDeclStmt : Type IDENTIFIER {printf("VarDeclStmt -> Type IDENTIFIER \n");}| 
              Type IDENTIFIER EQ Expression {printf("VarDeclStmt -> Type IDENTIFIER EQ Expression \n");}| 
              Type IDENTIFIER EQ ArrayConstant{printf("VarDeclStmt -> Type IDENTIFIER = ARRAYCONSTANT \n");}

Relation : LESS {printf("Relation -> < \n");}| 
           LESSEQ {printf("Relation -> <=\n");}| 
           BIGGER {printf("Relation -> > \n");}| 
           BIGGEREQ {printf("Relation -> >= \n");}| 
           EQQ {printf("Relation -> == \n");}| 
           NEQ {printf("Relation -> != \n");}
Condition : Expression {printf("Condition -> Expression \n");}| 
            Expression Relation Expression {printf("Condition -> Expression Relation Expression \n");}

%%
yyerror(char *s)
{	
	printf("Error parsing: %s\n",s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
	if(argc>1) yyin =  fopen(argv[1],"r");
	if(!yyparse()) fprintf(stderr, "\n\tParsing OK\n");
} 