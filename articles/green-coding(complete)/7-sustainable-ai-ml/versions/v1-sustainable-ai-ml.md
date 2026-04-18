# Sustainable AI/ML - Training Models Without Burning the Planet

Part 7 of my series on Sustainable Software Engineering...

## Opening Hook - The GPT-3 Problem

- Training GPT-3 emitted 552 tons of CO₂
- That's like driving 5 cars for their entire lifetime
- Or 120 round-trip flights from NYC to San Francisco
- And that's just ONE model, ONE training run
- We're training thousands of models every day
- The AI boom is also a carbon boom
- Real question: can we do ML without massive carbon costs?

## The AI Carbon Problem (Why This Matters)

- Training costs are insane (GPT-3 example)
- But inference costs at scale are worse
- ChatGPT serves millions of requests per day
- Each request costs compute
- Multiply that by every AI service
- Hardware matters: GPU vs TPU vs CPU efficiency
- The retraining problem (models go stale, need retraining)
- Nobody talks about this enough

## Model Efficiency Techniques

**Model Pruning**:
- Remove unnecessary weights (like trimming a tree)
- Can reduce model size by 90% with minimal accuracy loss
- Real example: BERT pruned from 110M to 11M parameters
- Still performs well on most tasks
- Way less compute for inference

**Quantization**:
- Reduce precision (FP32 → FP16 → INT8)
- 4x memory reduction, 2-4x speed improvement
- Minimal accuracy loss for most models
- TensorFlow Lite, PyTorch quantization
- Edge deployment becomes possible

**Knowledge Distillation**:
- Train small "student" model from large "teacher" model
- DistilBERT: 40% smaller, 60% faster, 97% of BERT's performance
- Teacher does heavy lifting once, student is efficient forever
- Like learning from a textbook instead of discovering everything yourself

**Neural Architecture Search (NAS)**:
- Automatically find efficient architectures
- EfficientNet: better accuracy with 10x fewer parameters
- MobileNet for mobile devices
- But NAS itself is expensive (ironic?)

## Training Optimization

**Mixed Precision Training**:
- Use FP16 instead of FP32 where possible
- 2x faster training, half the memory
- NVIDIA Tensor Cores optimize for this
- Automatic mixed precision in PyTorch/TensorFlow
- Minimal code changes, big impact

**Gradient Checkpointing**:
- Trade compute for memory
- Recompute activations instead of storing them
- Allows larger batch sizes
- Larger batches = fewer iterations = faster training
- Good for memory-constrained scenarios

**Efficient Batch Sizes**:
- Too small: underutilize GPU
- Too large: diminishing returns, memory issues
- Sweet spot varies by model and hardware
- Profile and experiment
- Gradient accumulation for effective large batches

**Learning Rate Schedules**:
- Warmup + decay strategies
- Converge faster with fewer epochs
- Fewer epochs = less compute = less energy
- Cosine annealing, one-cycle policy
- Can cut training time by 30-50%

**Early Stopping**:
- Stop when validation loss plateaus
- Don't waste compute on marginal improvements
- Patience parameter matters
- Monitor validation metrics closely
- Can save 20-40% of training time

## Carbon-Aware ML Training

**Schedule Training During Low-Carbon Hours**:
- Grid carbon intensity varies by time of day
- Solar peaks at noon, wind at night
- Train overnight in wind-heavy regions
- Train midday in solar-heavy regions
- Microsoft does this for large models (16% carbon reduction)

**Use Renewable-Heavy Regions**:
- AWS eu-north-1 (Stockholm): 13 gCO₂/kWh
- AWS us-east-1 (Virginia): 400 gCO₂/kWh
- 30x difference for same compute
- Move training to low-carbon regions
- Latency doesn't matter for batch training

**Pause/Resume Training**:
- Pause during high-carbon hours
- Resume during low-carbon hours
- Checkpointing makes this possible
- Requires orchestration (Kubernetes CronJobs?)
- Tradeoff: longer wall-clock time, lower carbon

## Inference Optimization

**Model Serving Efficiency**:
- Batch inference when possible
- Dynamic batching for real-time
- Model caching and reuse
- Quantized models for inference
- ONNX Runtime, TensorRT optimization

**Batch vs Real-Time Inference**:
- Batch: process 1000 items at once (efficient)
- Real-time: process 1 item immediately (responsive)
- Batch is 10-100x more efficient
- Use batch when latency allows
- Queue and batch user requests

**Edge Inference vs Cloud**:
- Edge: runs on user device (phone, IoT)
- Cloud: runs in data center
- Edge: no network transfer, uses device power
- Cloud: network transfer, uses grid power
- Tradeoff depends on model size and frequency

**Model Caching**:
- Cache model outputs for common inputs
- Embeddings, predictions, features
- Avoid recomputation
- Redis, Memcached for caching
- Cache hit rate matters

## Transfer Learning and Fine-Tuning

**Reuse Pre-Trained Models**:
- Don't train from scratch
- Use BERT, GPT, ResNet, etc.
- Fine-tune on your data
- 100x less compute than training from scratch
- Hugging Face model hub

**Few-Shot Learning**:
- Learn from few examples
- GPT-3 style prompting
- No fine-tuning needed
- Even more efficient
- Tradeoff: less customization

**Prompt Engineering vs Retraining**:
- Can you solve it with better prompts?
- Prompt engineering: zero compute
- Fine-tuning: some compute
- Training from scratch: massive compute
- Try prompts first

## MLOps Efficiency

**Experiment Tracking**:
- Track what you've tried
- Avoid redundant experiments
- MLflow, Weights & Biases
- Version models and datasets
- Learn from past experiments

**Model Registry**:
- Central repository for models
- Reuse models across teams
- Avoid duplicate training
- Version control for models
- Lifecycle management

**A/B Testing Efficiency**:
- Test on small sample first
- Scale up if promising
- Don't deploy bad models to 100% traffic
- Gradual rollout
- Monitor performance and cost

**Model Monitoring**:
- Detect model drift
- Retrain only when necessary
- Don't retrain on schedule
- Retrain when performance degrades
- Saves unnecessary retraining

## Hardware Selection

**GPU Efficiency**:
- A100: most efficient for large models
- V100: good middle ground
- T4: efficient for inference
- Older GPUs waste energy
- Upgrade hardware for efficiency

**TPU for Specific Workloads**:
- Google's Tensor Processing Units
- Optimized for TensorFlow
- Very efficient for certain models
- Not general purpose
- Consider for large-scale training

**CPU Inference for Small Models**:
- Don't use GPU for tiny models
- CPU is more efficient for small workloads
- GPU overhead not worth it
- Profile and compare

**Spot Instances for Training**:
- 70-90% cheaper than on-demand
- Can be interrupted
- Use checkpointing
- Restart automatically
- Huge cost and carbon savings

## Real-World Examples

**Hugging Face Model Efficiency Leaderboard**:
- Ranks models by efficiency
- Performance vs compute tradeoff
- Helps choose efficient models
- Community-driven

**Google Efficient Transformers**:
- Reformer, Linformer, Performer
- Reduce transformer complexity
- O(n²) → O(n log n) or O(n)
- Same tasks, less compute

**OpenAI GPT-3 Training Optimization**:
- Used mixed precision
- Optimized batch sizes
- Efficient parallelization
- Still expensive, but optimized

## Tradeoffs

**Model Accuracy vs Efficiency**:
- Smaller models = less accurate (usually)
- Quantization = slight accuracy loss
- Pruning = some accuracy loss
- Find acceptable tradeoff
- 1% accuracy loss for 10x efficiency?

**Training Time vs Carbon Cost**:
- Faster training = more GPUs = more energy
- Slower training = fewer GPUs = less energy
- But longer wall-clock time
- Opportunity cost matters
- Balance speed and efficiency

**Inference Latency vs Throughput**:
- Real-time: low latency, low throughput
- Batch: high latency, high throughput
- Batch is more efficient
- Use batch when possible
- Real-time only when necessary

Target: ~2,000 words when complete
