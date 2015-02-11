# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 22:04:01 2014
Thoughts:
- Every neuron is connected to other neurons.
- Connections can either be excitatory or inhibitory.
- Neurons should die if they haven't been activated in a while.
- Connection strength can be modified based on frequency of coactivation.

@author: taylorsalo
"""
import threading
import time
import numpy as np
from datetime import datetime

default_weight = 0.5

class Neuron:
    def __init__(self, name, connectors=[]):
        self.name = name
        self.fired_last = datetime.strptime('16Sep2012', '%d%b%Y')
        self.potential_at_hillock = 0
        self.connections = {}
        if connectors:
            if type(connectors) == list:
                for connector in connectors:
                    self.connections[connector] = default_weight
            else:
                for connector in connectors.keys():
                    self.connections[connector] = connectors[connector]

    def add_connection(self, connector, weight):
        self.connections[connector] = weight

    def psp(self, val, brain):
        # Evaluate current depolarization levels and fire if both above
        # threshold and outside refractory period.
#        print(self.name + " has potential_at_hillock of " + str(self.potential_at_hillock) + "\n")
        
        # Refractory period
        time_elapsed = datetime.now() - self.fired_last
        seconds_elapsed = time_elapsed.total_seconds() 
        if seconds_elapsed > 5:
            in_refractory_period = False
            self.potential_at_hillock = val
        else:
            in_refractory_period = True
        
        # Fire if above threshold
        if self.potential_at_hillock > 10 and not in_refractory_period:
            print(self.name + " fired!\n")
            self.fire(brain)

    def fire(self, brain):
        self.fired_last = datetime.now()
        self.potential_at_hillock = 0
        thread = {}
        for connector in self.connections:
            # Generate post-synaptic potentials for every efferent synapse.
            print(self.name + " fired to " + connector + "\n")
            thread[connector] = threading.Thread(target=self.create_psp, args=(brain, connector,))
            thread[connector].daemon = True
            thread[connector].start()

    def create_psp(self, brain, connector):
        # Generate post-synaptic potential and slowly returning to baseline.
        brain.neurons[connector].psp(brain.neurons[connector].potential_at_hillock + self.connections[connector], brain)
        connection_sign = np.sign(self.connections[connector])
        for current_input in np.arange(0, np.abs(self.connections[connector]), 1):
            time.sleep(1)
            last_fired = brain.neurons[connector].fired_last - datetime.now()
            if last_fired.total_seconds() < 5:
                break

            if connection_sign == 1:
                brain.neurons[connector].psp(brain.neurons[connector].potential_at_hillock - 1, brain)
            else:
                brain.neurons[connector].psp(brain.neurons[connector].potential_at_hillock + 1, brain)


class Brain:
    def __init__(self):
        self.neurons = {}
        self.neuron_count = 0

    def add_neuron(self, neuron):
        self.neurons[neuron] = Neuron(neuron)
        self.neuron_count += self.neuron_count

    def add_connection(self, pre, post, weight):
        self.neurons[pre].add_connection(post, weight)

taylor = Brain()
taylor.add_neuron('Neuron 1')
taylor.add_neuron('Neuron 2')
taylor.add_neuron('Neuron 3')
taylor.add_neuron('Neuron 4')
taylor.add_neuron('Neuron 5')

taylor.add_connection('Neuron 1', 'Neuron 4', 5)
taylor.add_connection('Neuron 2', 'Neuron 4', 5)
taylor.add_connection('Neuron 3', 'Neuron 4', 5)

taylor.add_connection('Neuron 2', 'Neuron 5', 5)
taylor.add_connection('Neuron 3', 'Neuron 5', 5)
taylor.add_connection('Neuron 4', 'Neuron 5', 5)

taylor.add_connection('Neuron 5', 'Neuron 1', -5)

neurons_to_fire = ['Neuron 1', 'Neuron 2', 'Neuron 3']
for neuron in neurons_to_fire:
    taylor.neurons[neuron].fire(taylor)

time.sleep(1)

#while taylor.neurons["Neuron 1"].potential_at_hillock != 0:
#    print("Neuron 1 has potential_at_hillock of " + str(taylor.neurons["Neuron 1"].potential_at_hillock))
#    time.sleep(1)
print("Neuron 1 has potential_at_hillock of " + str(taylor.neurons["Neuron 1"].potential_at_hillock))
