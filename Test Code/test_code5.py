# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 20:27:50 2022

@author: Cyrus
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 19:47:50 2022

@author: Cyrus
"""
#create reinforcer set (these are based on which target is reinforced)
#create behavior set (these are based on which target behavior is emitted)
import numpy

class Output:
    subclasses = {}
    stream_log = []
    output_column_titles = []
    current_schedule = None
    
    @classmethod
    def set_current_schedule(cls,current_schedule):
        cls.current_schedule = current_schedule
        
    @classmethod
    def generate_empty_stream_log(cls,max_gen,output_items):
        cls.stream_log = numpy.zeros([max_gen,output_items])
   
    @classmethod
    def set_output_columns(cls,max_gen,output_items):
        cls.stream_log = numpy.zeros([max_gen,output_items])
    
    @classmethod
    def register_subclass(cls, output_type):
        def decorator(subclass):
            cls.subclasses[output_type] = subclass
            return subclass
      
        return decorator    
    
    @classmethod
    def capture(cls, output_type, *args, **kargs):
        if output_type not in cls.subclasses:
            raise ValueError('Bad output type {}'.format(output_type))
      
        return cls.subclasses[output_type](*args, **kargs)

    # @classmethod
    # def capture(cls, output_type, schedule, generation,\
    #             emitted_bx, reinforcers, behaviors, *args, **kargs):
    #     if output_type not in cls.subclasses:
    #         raise ValueError('Bad output type {}'.format(output_type))
      
    #     return cls.subclasses[output_type](schedule, generation,\
    #                                        emitted_bx, reinforcers, behaviors,*args, **kargs)

@Output.register_subclass('stream_output')
class Stream(Output):
    def __init__(self):
       pass
   
    def __new__(self, schedule, generation, emitted_bx, \
                reinforcers, behaviors,*args, **kargs):
        Stream.capture(schedule, generation, emitted_bx, \
                       reinforcers, behaviors,*args, **kargs)
        
    
    def capture(schedule, generation, emitted_bx, \
                reinforcers, behaviors,*args, **kargs):
        
        if Output.current_schedule == None:
            Output.set_current_schedule = schedule
        elif Output.current_schedule != schedule:
            raise ValueError("schedule changed occured without export occuring!")
            
        x_index = generation-1
        #emitted, bx, R1, R2, B1, B2 
        
        # Output.capture("stream_output",1,2,3,[4,5,6],[7,8])
        # print("schedule = ", schedule) #1
        # print("generation = ", generation) #2
        # print("emitted_bx = ", emitted_bx) #3
        # print("reinforcers = ", reinforcers) #4, 5, 6 
        # print("behaviors = ", behaviors) #7, 8
        
        counter = 0
        Output.stream_log[x_index].put([counter],[emitted_bx])
    
        counter += 1
        for given in reinforcers:
            Output.stream_log[x_index].put([counter],[given])
            counter += 1
        for hit in behaviors:
            Output.stream_log[x_index].put([counter],[hit])
            counter += 1
 ##############################################################################

Output.generate_empty_stream_log(4,6)

Output.capture("stream_output",1,2,3,[4,5,6],[7,8])

print(Output.stream_log[:,:])





       