import torch
from typing import Callable
from numpy.random import default_rng
from torch import Tensor, Size
from torch.distributions.laplace import Laplace

rng = default_rng()


def gaussian(sigma: float) -> Callable[[Size], Tensor]:
    """
    Normal distribution
    :param sigma: stdev
    :return: noise function
    """
    def noise_func(size):
        # return torch.randn(size, device='cuda') * sigma
        return torch.from_numpy(rng.normal(0.0, sigma, size=size)).float().to('cuda')
    return noise_func


def abs_gaussian(sigma: float) -> Callable[[Size], Tensor]:
    """
    Absolute value of normal distribution
    :param sigma: stdev
    :return: noise function
    """
    def noise_func(size):
        return (torch.randn(size, device='cuda') * sigma).abs()
    return noise_func


def uniform(a: float) -> Callable[[Size], Tensor]:
    """
    Uniform distribution
    :param a: lower limit
    :return: noise function
    """
    def noise_func(size):
        return (2 * torch.rand(size, device='cuda') * a) + a
    return noise_func


def constant(a: float) -> Callable[[Size], Tensor]:
    """
    Constant noise
    :param a: constant
    :return: noise function
    """
    def noise_func(size):
        return torch.ones(size, device='cuda') + float(a)
    return noise_func


def laplace(scale: float) -> Callable[[Size], Tensor]:
    """
    Laplace distribution
    :param scale: scale
    :return: noise function
    """
    m = Laplace(0, scale)

    def noise_func(size):
        noise = m.sample(size)
        return noise.to('cuda')
    return noise_func


def bernoulli(p: float) -> Callable[[Size], Tensor]:
    """
    Bernoulli distribution
    :param p: probablity of 1
    :return: noise function
    """
    def noise_func(size):
        noise = torch.lt(torch.rand(size), torch.ones(size) * (1 - p)).float().cuda()
        return noise
    return noise_func


NOISE_FUNCTIONS = {
    'gaussian': gaussian,
    'abs_gaussian': abs_gaussian,
    'uniform': uniform,
    'constant': constant,
    'laplace': laplace,
    'bernoulli': bernoulli
}
