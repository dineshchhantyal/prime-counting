#!/bin/bash
#SBATCH --job-name=prime_benchmarks
#SBATCH --output=logs/prime_benchmarks_%j.out
#SBATCH --error=logs/prime_benchmarks_%j.err
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=16G
#SBATCH -p genx

# Activate your environment if needed
source /mnt/home/dchhantyal/prime-counting/.venv/bin/activate

mkdir -p logs

echo "Benchmarking all prime counting methods..."

METHODS=(
    "1:LessThanSqrt"
    "2:PrimeLessThanSqrt"
    "3:SieveClassic"
    "4:SievePartitioned"
    "5:MeisselLehmer"
)

# Submit each method as a separate SLURM job for parallel execution
for entry in "${METHODS[@]}"; do
    IFS=':' read -r num name <<< "$entry"
    echo "========================================"
    echo "Submitting job for method $num ($name)"
    echo "========================================"
    sbatch --job-name=prime_${name} \
        --output=logs/${name}_benchmark_%j.out \
        --error=logs/${name}_benchmark_%j.err \
        --time=2-00:00:00 \
        --cpus-per-task=1 \
        -p genx \
        --mem=128G \
        --wrap="source /mnt/home/dchhantyal/prime-counting/.venv/bin/activate && \
        python custom_tests/test_with_command.py $num > logs/${name}_benchmark.log 2>&1"
    echo "Job for method $num ($name) submitted."
    echo "========================================"
done

echo "All benchmarks submitted. Check logs/ for results."