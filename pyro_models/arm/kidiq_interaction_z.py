# model file: example-models/ARM/Ch.4/kidiq_interaction_z.stan
import torch
import pyro
import pyro.distributions as dist

def init_vector(name, dims=None):
    return pyro.sample(name, dist.Normal(torch.zeros(dims), 0.2 * torch.ones(dims)).to_event(1))



def validate_data_def(data):
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'kid_score' in data, 'variable not found in data: key=kid_score'
    assert 'mom_hs' in data, 'variable not found in data: key=mom_hs'
    assert 'mom_iq' in data, 'variable not found in data: key=mom_iq'
    # initialize data
    N = data["N"]
    kid_score = data["kid_score"]
    mom_hs = data["mom_hs"]
    mom_iq = data["mom_iq"]

def transformed_data(data):
    # initialize data
    N = data["N"]
    kid_score = data["kid_score"]
    mom_hs = data["mom_hs"]
    mom_iq = data["mom_iq"]
    z_mom_hs = (mom_hs - torch.mean(mom_hs)) / (2 * torch.std(mom_hs));
    z_mom_iq = (mom_iq - torch.mean(mom_iq)) / (2 * torch.std(mom_iq));
    inter    = z_mom_hs * z_mom_iq;
    data["z_mom_hs"] = z_mom_hs
    data["z_mom_iq"] = z_mom_iq
    data["inter"] = inter

def init_params(data):
    params = {}
    params["beta"] = init_vector("beta", dims=(4)) # vector

    return params

def model(data, params):
    # initialize data
    N = data["N"]
    kid_score = data["kid_score"]
    mom_hs = data["mom_hs"]
    mom_iq = data["mom_iq"]
    # initialize transformed data
    z_mom_hs = data["z_mom_hs"]
    z_mom_iq = data["z_mom_iq"]
    inter = data["inter"]

    # init parameters
    beta = params["beta"]

    sigma =  pyro.sample("sigma", dist.HalfCauchy(torch.tensor(2.5)))
    with pyro.plate("data", N):    
        kid_score = pyro.sample('obs', dist.Normal(beta[0] + beta[1] * z_mom_hs + beta[2] * z_mom_iq + beta[3] * inter, sigma), obs=kid_score)
