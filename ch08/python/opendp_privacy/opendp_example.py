import opendp.prelude as dp

def main():
    # 1. Enable 'contrib' features
    # Many OpenDP constructors are currently in the 'contrib' module
    dp.enable_features("contrib")

    # 2. Define the sample data
    # We use a list of values (e.g., ages or scores)
    data = [22.0, 35.0, 45.0, 50.0, 28.0, 60.0, 42.0, 38.0]
    
    # 3. Define privacy parameters
    # Epsilon (ε) controls the privacy-utility trade-off
    epsilon = 1.0
    
    # Differential privacy requires known bounds and dataset size
    # to calculate the sensitivity of the operation
    data_bounds = (0.0, 100.0)
    data_size = len(data)

    # 4. Build the transformation pipeline
    # - input_space: Vector of floats with symmetric distance
    # - clamp: Bounds values to [0, 100]
    # - resize: Ensures the dataset size is fixed at data_size
    # - mean: Computes the average
    input_space = (
        dp.vector_domain(dp.atom_domain(T=float, nan=False)),
        dp.symmetric_distance()
    )
    
    preprocess = (
        input_space >>
        dp.t.then_clamp(bounds=data_bounds) >>
        dp.t.then_resize(size=data_size, constant=sum(data_bounds)/2.0) >>
        dp.t.then_mean()
    )
    
    # 5. Determine the noise scale for the requested epsilon
    # We use the Laplace mechanism to satisfy the privacy budget
    scale = dp.binary_search_param(
        lambda s: preprocess >> dp.m.then_laplace(scale=s),
        d_in=1,
        d_out=epsilon
    )
    
    # 6. Create the final measurement
    measurement = preprocess >> dp.m.then_laplace(scale=scale)
    
    # 7. Execute the measurement on the data
    dp_mean = measurement(data)
    
    actual_mean = sum(data) / len(data)
    print(f"Actual Mean: {actual_mean:.2f}")
    print(f"Differentially Private Mean: {dp_mean:.2f}")

if __name__ == "__main__":
    main()
