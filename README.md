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
what is bc and how it was implemented

[gif: car is driving on a tortuous road]

#### Dataset Aggregation (DAgger)
how we are going to benefit from dagger

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
talk about env

[top-view picture of the env]

#### Conditional Imitation Learning
how it was implemented and the differences with typical BC

[the model]

[gif: car driving]
  
### Carla Town
<img src="https://npm3d.fr/storage/pages/September2021/Town01.jpg" width="500px">
talk about env

[top-view picture of the env]

#### Flexible conditions
how we denote them

[image of the carla dataset settings]

#### Path Prediction
the model

[image: predicted path and the given inputs]

#### Translator
the model

[gif car driving in the env]

## References

1. Codevilla, F., Müller, M., López, A., Koltun, V., and Dosovitskiy, A., “End-to-end Driving via Conditional Imitation Learning”, <i>arXiv e-prints</i>, 2017.
2. CIL
3. new CIL
