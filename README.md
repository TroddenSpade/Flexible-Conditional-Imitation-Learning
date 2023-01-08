# Flexible Conditional Imitation Learning
The purpose of this project is to implement the Conditional Imitation Learning on various scenarios with `Airsim Car` plugin and `Carla` Environments. The original Conditional Imitation Learning propose a method in which a single navigatorial command is employed to take a certain action in perplexing situations. Instead, to increase the flexibility, this project concentrates on conditions similar to a path--a set of points on a plane--whereby we could present any kind of turns and velocities. 


## Requirements
* Tensorflow
* Unreal Engine 4 (UE4)
* [Airsim](https://microsoft.github.io/AirSim/)
* [Carla](http://carla.org)


## Experiments
Three different strategies are assessed.

### Mountainous UE4 Environment
<img src="https://cdn1.epicgames.com/ue/item/store_LandscapeMountains_screenshot_2-1920x1080-5176d0fbdf122cf4bfdb307d7c79e57a.png?resize=1&w=1920" width="500px">

In [this environment](https://www.unrealengine.com/marketplace/en-US/product/landscape-mountains), the goal is to create an autonumous agent to drive through a tirtuous and mountainous road with the help of `Behavioral Cloning` and `Dataset Aggregation` approaches.


#### Behavorial Cloning
[//]: <> (what is bc and how it was implemented)


#### Dataset Aggregation (DAgger)
[//]: <> (how we are going to benefit from dagger)

| <img src="https://github.com/TroddenSpade/Flexible-Conditional-Imitation-Learning/blob/main/assets/dagger.gif?raw=true"> |
| :--: |
| Collecting Data for Dataset Aggregation |

#### Demo

| <img src="https://github.com/TroddenSpade/Flexible-Conditional-Imitation-Learning/blob/main/assets/mountanous-auto-car.gif?raw=true"> |
| :--: |
| Autonomous Car Driving in Mountainous Environment |

### Neighborhood UE4 Env
<img src="https://cdn1.epicgames.com/ue/product/Screenshot/storeModularNeighborhoodscreenshot12-1920x1080-e6253c36e6fd0e988be3160f4b23e485.png?resize=1&w=1920" width="500px">

[This Env](https://www.unrealengine.com/marketplace/en-US/product/modular-neighborhood-pack)

[//]: <> (talk about env)


#### Conditional Imitation Learning
[//]: <> (how it was implemented and the differences with typical BC)

  
### Carla Town
<img src="https://npm3d.fr/storage/pages/September2021/Town01.jpg" width="500px">


#### Flexible conditions
<img src="https://user-images.githubusercontent.com/33734646/211207458-ffafcf8c-6277-4860-9b70-064c481f15dc.jpeg" width="500px">


#### Path Prediction

![Car](https://user-images.githubusercontent.com/33734646/211207480-aa3eb135-7d19-410c-bf5b-eb58a1881972.png)


#### Translator


## References

1. Codevilla, F., Müller, M., López, A., Koltun, V., and Dosovitskiy, A., “End-to-end Driving via Conditional Imitation Learning”, <i>arXiv e-prints</i>, 2017.
2. Codevilla, F., Santana, E., Lopez, A., & Gaidon, A. (2019). Exploring the limitations of behavior cloning for autonomous driving. Proceedings of the IEEE International Conference on Computer Vision, 2019-Octob(Cvc), 9328–9337. https://doi.org/10.1109/ICCV.2019.00942
3. Rhinehart, N., McAllister, R., & Levine, S. (2018). Deep Imitative Models for Flexible Inference, Planning, and Control. 1, 1–19. http://arxiv.org/abs/1810.06544
