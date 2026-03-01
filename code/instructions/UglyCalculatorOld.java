package com.calculator;
import java.util.*;public class UglyCalculator{private int result=0;private String operation;
private List operations=new ArrayList();//BAD: raw type, no generics
//No javadoc
public void add(int a,int b){result=a+b;operations.add("add");}
public void subtract(int a, int b) {
result = a - b;
    operations.add("subtract");
}
	public void multiply(int x,int y){result=x*y;operations.add("multiply");}
   	public  void   divide(int numerator,int denominator){
if(denominator==0){System.out.println("error");}else{result=numerator/denominator;operations.add("divide");}}
public Integer getResult(){return result;}//using Integer instead of Optional
public String getLastOperation(){return operation;}//will return null
public void clearAll(){result=0;operation=null;operations.clear();}
public void printHistory(){for(Object op:operations){System.out.println(op);}}
//Catching generic Exception
public void performCalculation(String op,int a,int b){try{if(op.equals("add")){add(a,b);}else if(op.equals("sub")){subtract(a,b);}else if(op.equals("mul")){multiply(a,b);}else if(op.equals("div")){divide(a,b);}}catch(Exception e){System.out.println("something went wrong");}}
public static void main(String[] args){UglyCalculator calc=new UglyCalculator();calc.add(10,20);calc.subtract(50,30);calc.multiply(5,6);calc.divide(100,5);System.out.println("Result: "+calc.getResult());calc.printHistory();}
}
