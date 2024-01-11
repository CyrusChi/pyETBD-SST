# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 21:32:19 2022

@author: Cyrus
"""
# import numpy

# mean = 100

# counter = 0
# for a in range(0,1000):
#     counter = counter + \
#     (-1 * mean * numpy.log(1 - numpy.random.random()))

# final_mean = counter / 1000 
# print ("the final mean is ", final_mean)
import numpy

mean = 10
lista = []
for index in range(100):
    a = -1 * mean * numpy.log(1 - numpy.random.random())
    lista.append(a)
    print("a = ", a)
print("average of a = ", sum(lista)/len(lista) )

# def send_message(message_type, params):
#     message = BaseMessage.create(message_type, params)
#     message.send()
  
# def observe_environment(observation_type, *args, **kargs):
#     observed_se = Observation.look(observation_type, *args, **kargs)
#     return observed_se

# class Observation(Organism):
#     subclasses = {}
    
#     @classmethod
#     def register_subclass(cls, observation_type):
#         def decorator(subclass):
#             cls.subclasses[observation_type] = subclass
#             return subclass
      
#         return decorator    
    
#     @classmethod
#     def look(cls, observation_type, near_registry, *args, **kargs):
#         if observation_type not in cls.subclasses:
#             raise ValueError('Bad observation type {}'.format(observation_type))
      
#         return cls.subclasses[observation_type](*args, **kargs)

# @Observation.register_subclass('observe_upto_five')
# class Observe_Upto_Five(Observation):
#     if len(near_registry)    
    
    
# class BaseMessage():
#     subclasses = {}

#     @classmethod
#     def register_subclass(cls, message_type):
#         def decorator(subclass):
#             cls.subclasses[message_type] = subclass
#             return subclass
      
#         return decorator
      
#     @classmethod
#     def create(cls, message_type, params):
#         if message_type not in cls.subclasses:
#             raise ValueError('Bad message type {}'.format(message_type))
      
#         return cls.subclasses[message_type](params)
      
      
# @BaseMessage.register_subclass('chat')
# class ChatMessage(BaseMessage):
#     pass
  
# @BaseMessage.register_subclass('email')
# class EmailMessage(BaseMessage):
   
#     pass
  
# @BaseMessage.register_subclass('phone')
# class PhoneMessage(BaseMessage):
#     pass
      
