# schedule-GA

Details about the program:
    - We assumed :
        A)Hard constraint that implemented in [2], it is performed after each crossover or mutation operations.
        B)Soft constraints that implemented in [3-5], they increase some value called penalty to use it in fit operation.
        C)Fittness function is : (Fittness=1/(1+penalty)), it should be maximized

    - Some details about some functions we used:        
        1)tech_sub:contains pairs of (Teacher name, Subject name).
        2)hardconstraint(ch): ensures that a teacher can't be in different classes at the same time.
        3)soft1(ch): increase the penalty if a teacher has more than 23 , 20 lectures per week for all classes.
        4)soft2(tech_count): increase the penalty in case of there is uneven total time slot for all teachers in the same field.
        5)soft3(ch): increase the penalty if a course was held in more than 2 time-slots in a day for one class from a prededefined subjects,
                      and more than one time.
        6)GA(chromosomeNo,classNo,mx,mp,iterations) : { chromosomeNo: the number of chromosomes in the generation,
                                                        classNo     : the number of classes in the chromosome,
                                                        mx          : the probability of crossover,
                                                        mp          : the probability of mutation,
                                                        iterations  : the number of iterations }            
        
    - Chromosome structure:
        The chromosome consists of classNo classes, each class has 7 lectures daily, 5 days weekly.

    - References:
        [1] https://bit.ly/35OnnnH
