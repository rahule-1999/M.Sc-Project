import bilby
import matplotlib.pyplot as plt


duration = 4
sampling_frequency = 2048
outdir = "visualising_the_results"
label = "example"

injection_parameters = dict(
    mass_1=36.0,
    mass_2=29.0,
    a_1=0.4,
    a_2=0.3,
    tilt_1=0.5,
    tilt_2=1.0,
    phi_12=1.7,
    phi_jl=0.3,
    luminosity_distance=1000.0,
    theta_jn=0.4,
    phase=1.3,
    ra=1.375,
    dec=-1.2108,
    geocent_time=1126259642.413,
    psi=2.659,
)

waveform_arguments = dict(
    waveform_approximant="IMRPhenomXP", 
    reference_frequency=50.0,  
)

waveform_generator = bilby.gw.waveform_generator.WaveformGenerator(
    sampling_frequency=sampling_frequency,
    duration=duration,
    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
    parameters=injection_parameters,
    waveform_arguments=waveform_arguments,
)

ifos = bilby.gw.detector.InterferometerList(["H1", "L1"])
ifos.set_strain_data_from_power_spectral_densities(
    duration=duration,
    sampling_frequency=sampling_frequency,
    start_time=injection_parameters["geocent_time"] - 2,
)
_ = ifos.inject_signal(
    waveform_generator=waveform_generator, parameters=injection_parameters
)

priors = bilby.gw.prior.PriorDict(injection_parameters.copy())
priors["mass_1"] = bilby.core.prior.Uniform(25, 40, "mass_1")
priors["mass_2"] = bilby.core.prior.Uniform(25, 40, "mass_2")
#priors["a_1"] = bilby.core.prior.Uniform(0, 1, "a_1")
priors["luminosity_distance"] = bilby.core.prior.Uniform(400, 2000, "luminosity_distance")
print(len(priors))

likelihood = bilby.gw.likelihood.GravitationalWaveTransient(
    interferometers=ifos, waveform_generator=waveform_generator
)

result = bilby.core.sampler.run_sampler(
    likelihood=likelihood,
    priors=priors,
    sampler="dynesty",
    npoints=100,
    injection_parameters=injection_parameters,
    outdir=outdir,
    label=label,
    sample="unif",
)

result.plot_corner(save=True)
plt.show()
plt.close()