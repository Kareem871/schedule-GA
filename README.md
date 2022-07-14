# schedule-GA
## Assumptions:
* Hard constraint that implemented in function 2 (From functions list below), it is performed after each crossover or mutation operations.
* Soft constraints that implemented in functions 3-5, they increase some value called penalty to use it in fit operation.
* Fittness function is : (Fittness=1/(1+penalty)), which should be maximized.

## Functions:
1- tech_sub:contains pairs of (Teacher name, Subject name).<br/>
2- hardconstraint(ch): ensures that a teacher can't be in different classes at the same time.<br/>
3- soft1(ch): increase the penalty if a teacher has more than 23 , 20 lectures per week for all classes.<br/>
4- soft2(tech_count): increase the penalty in case of there is uneven total time slot for all teachers in the same field.<br/>
5- soft3(ch): increase the penalty if a course was held in more than 2 time-slots in a day for one class from a prededefined subjects and more than one time.<br/>
6- GA(chromosomeNo,classNo,mx,mp,iterations) : <br/>
{ <br/>
chromosomeNo: the number of chromosomes in the generation,<br/>
classNo     : the number of classes in the chromosome,<br/>
mx          : the probability of crossover,<br/>
mp          : the probability of mutation,<br/>
iterations  : the number of iterations<br/>
}<br/>            
        
## Chromosome structure:
        The chromosome consists of classNo classes, each class has 7 lectures daily, 5 days weekly.

# Reference:
        [1] https://bit.ly/35OnnnH
