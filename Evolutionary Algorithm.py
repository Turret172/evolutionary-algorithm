#required modules and functions
import random, time

#outputs True or False with a given chance (in percent)
def chance(x):
    r = random.randint(0, 999999999)/10000000
    if r < x:
        return True
    else:
        return False

#evaluates which item is the shortest, and returns it
def shortest(a, b):
    if len(a) > len(b):
        return b
    else:
        return a

#calculates the similarity of two items
def likeness(a, b):
    l = 0
    for i in range(len(shortest(a, b))):
        if a[i] == b[i]:
            l+=1
    return l

##### built-in evolutionary functions

def generateOrganisms(amount, size):
    #organism's DNA is stored as a string
    #organisms are stored as a list of these strings
    organism, organisms = '', []

    #generates initial organism
    for i in range(size):
        organism += '0'

    #fills list with instances of this initial organism
    for i in range(amount):
        organisms.append(organism)

    #output must be a list
    return organisms

def evaluateOrganisms(organisms, evaluationFunction, dna_target):
    #evaluationFunction is the function that is used to score the organism
    #it must return an int or float
    scores = []

    #creates a list of tuples in format (organism, score)
    for organism in organisms:
        scores.append((organism, evaluationFunction(organism, dna_target)))

    #sorts the list based on the second value of each tuple, in ascending order
    #this essentially "ranks" the organisms, with the worst at the start and the best at the end
    #outputs an ordered list of organisms without the scores
    sorted_organism_base = sorted(scores, key=lambda tpl: tpl[1])
    sorted_organisms = [tpl[0] for tpl in sorted_organism_base]

    best_organism = sorted_organisms[-1]
    random_organism = random.choice(sorted_organisms)
    worst_organism = sorted_organisms[0]

    #returns sorted list, along with the best, random, and worst organisms and their scores, and all the sorted organisms with scores
    best = (best_organism, evaluationFunction(best_organism, dna_target))
    ran = (random_organism, evaluationFunction(random_organism, dna_target))
    worst = (worst_organism, evaluationFunction(worst_organism, dna_target))
    #main output must be a list
    return sorted_organisms, best, ran, worst, sorted_organism_base

def killOrganisms(organisms, amount_to_kill):
    #kills off a certain amount of organisms
    #when given the output of the evaluateOrganisms function, this function kills the worst organisms

    for i in range(amount_to_kill):
        #removes the first in the list
        del organisms[0]

    #returns shortened list of organisms
    return organisms

def breedOrganisms(organisms, population_target, error_rate):
    #breeding process does not complete until the population target is reached
    #note that the error rate is in PERCENT, and not a value from 0 to 1.
    while len(organisms) < population_target:
        #selects two random organisms (note that nothing stops them from being the same organism)
        selected_a = random.choice(organisms)
        selected_b = random.choice(organisms)
        new_organism = ''

        #generates a new organism from mixing the DNA of the two selected organisms
        for i in range(len(selected_a)):
            #if a mutation occurs, use a random value instead of an inherited value
            if chance(error_rate):
                new_organism += str(random.randint(0, 9))
            #50% chance of inheriting a segment of DNA from organism A
            #otherwise, inherit segment from organism B
            elif chance(50):
                new_organism += selected_a[i]
            else:
                new_organism += selected_b[i]

        #adds the new organism to the list of existing ones
        organisms.append(new_organism)

    #returns the new list of organisms
    return organisms

##### main config

error_rate = 2 # 2% mutations
population = 1000 # the simulation will maintain 1000 organisms
dna_length = 96 # the length of the organism DNA
kill_rate = 50 # 50% of organisms will be killed
eval_func = likeness # evaluation function is previously defined likeness function
gen_delay = 1 # amount of time in seconds the program waits before starting another generation
stop_if_target_reached = False # does the simulation stop if the target is reached?

#####automatic config
#DNA target is currently arbitrary, in this case it is 96 digits of pi
dna_target = '314159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211'
kill_amount = int(population * (kill_rate / 100))
organisms = generateOrganisms(population, dna_length)
generation = 0

#####main simulation
while True:
    #increments the generation counter
    generation += 1

    #evaluates and sorts organists
    organisms, best, ran, worst, orgs_with_sc = evaluateOrganisms(organisms, eval_func, dna_target)
    score_list = [tpl[1] for tpl in orgs_with_sc]

    #prints the status of the simulation to the console
    print(f"Generation {generation}\n")
    print(f"Target DNA:         {dna_target}")
    print(f"Best organism DNA:  {best[0]}")
    print(f"Random organism DNA:{ran[0]}")
    print(f"Worst organism DNA: {ran[0]}")
    print(f"Best, random, and worst scores: {best[1]}/{dna_length}, {ran[1]}/{dna_length}, {worst[1]}/{dna_length}")
    print(f"Average score: {sum(score_list)/len(score_list):.3f}/{dna_length}\n\n\n")

    #if the target DNA is reached, and the "stop if target reached" option is enabled, it exits the loop
    if best[0] == dna_length and stop_if_target_reached:
        break

    #introduces natural selection into the process, which, with time, drives evolution
    organisms = killOrganisms(organisms, kill_amount)
    organisms = breedOrganisms(organisms, population, error_rate)

    #waits until next gen, as no delay would be too fast for a human to read the information presented
    time.sleep(gen_delay)

print("Target has been reached, simulation complete.")
input('Press ENTER to quit. ')
