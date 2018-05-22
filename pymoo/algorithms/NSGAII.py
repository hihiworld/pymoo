from pymoo.algorithms.genetic_algorithm import GeneticAlgorithm
from pymoo.operators.crossover.bin_uniform_crossover import BinaryUniformCrossover
from pymoo.operators.crossover.real_simulated_binary_crossover import SimulatedBinaryCrossover
from pymoo.operators.mutation.bin_bitflip_mutation import BinaryBitflipMutation
from pymoo.operators.mutation.real_polynomial_mutation import PolynomialMutation
from pymoo.operators.sampling.bin_random_sampling import BinaryRandomSampling
from pymoo.operators.sampling.real_random_sampling import RealRandomSampling
from pymoo.operators.selection.tournament_selection import TournamentSelection
from pymoo.operators.survival.rank_and_crowding import RankAndCrowdingSurvival
from pymoo.rand import random
from pymoo.util.dominator import Dominator


class NSGAII(GeneticAlgorithm):
    def __init__(self, var_type, pop_size=100, verbose=1):

        if var_type == "real":
            super().__init__(
                pop_size,
                RealRandomSampling(),
                TournamentSelection(f_comp=comp_by_rank_and_crowding),
                SimulatedBinaryCrossover(),
                PolynomialMutation(),
                RankAndCrowdingSurvival(),
                verbose=verbose
            )
        elif var_type == "binary":
            super().__init__(
                pop_size,
                BinaryRandomSampling(),
                TournamentSelection(f_comp=comp_by_rank_and_crowding),
                BinaryUniformCrossover(),
                BinaryBitflipMutation(),
                RankAndCrowdingSurvival(),
                verbose=verbose,
                eliminate_duplicates=True
            )


def comp_by_rank_and_crowding(pop, indices, data):
    if len(indices) != 2:
        raise ValueError("Only implemented for binary tournament!")

    first = indices[0]
    second = indices[1]

    if data.rank[first] < data.rank[second]:
        return first
    elif data.rank[second] < data.rank[first]:
        return second
    else:
        if data.crowding[first] > data.crowding[second]:
            return first
        elif data.crowding[second] > data.crowding[first]:
            return second
        else:
            return indices[random.randint(0, 2)]


def comp_by_dom_and_crowding(pop, indices, data):
    if len(indices) != 2:
        raise ValueError("Only implemented for binary tournament!")

    first = indices[0]
    second = indices[1]

    rel = Dominator.get_relation(pop.F[first, :], pop.F[second, :])

    if rel == 1:
        return first
    elif rel == -1:
        return second
    else:
        if data.crowding[first] > data.crowding[second]:
            return first
        elif data.crowding[second] > data.crowding[first]:
            return second
        else:
            return indices[random.randint(0, 2)]
