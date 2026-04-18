# Teams Post — Sustainable AI/ML

**Channel**: Jabil Developer Network — Architecture Community
**Subject Line**: Training GPT-3 emitted 552 tons of CO₂. Your models probably aren't much better.
**Featured Image**: `images/featured_image.png`
**Article URL**: https://medium.com/gitconnected/sustainable-ai-ml-training-to-inference-while-minimizing-carbon-4e033d50e127

---

![Featured Image](../images/featured_image.png)

## The AI Carbon Problem Nobody Talks About

Every company is training models now. Each training run burns compute. Each inference request burns more. And most teams retrain on a schedule whether the model needs it or not.

One team I worked with was retraining weekly. The model had been stable for months. Switching to performance-based retraining cut their compute by 80%.

## Quick Wins That Actually Move the Needle

- **Pruning**: 90% smaller models, 95% accuracy retained
- **Quantization**: FP32 → INT8 gives you 4x speedup with 1-2% accuracy loss
- **Mixed precision training**: 2x faster with 3 lines of code
- **Carbon-aware scheduling**: Training during low-carbon hours cut Microsoft's emissions 16%
- **Region selection**: Stockholm at 13 gCO₂/kWh vs Virginia at 400 gCO₂/kWh

The tradeoff worth internalizing: 95% accuracy with 10x efficiency often beats 98% accuracy at 1x efficiency.

**Part 7 of the Sustainable Software Engineering series** — [Read the full article](https://medium.com/gitconnected/sustainable-ai-ml-training-to-inference-while-minimizing-carbon-4e033d50e127)
