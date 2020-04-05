# StatQuest Notes
> last updated by Wei, Apr 2020

### Gradient Boost
#### main ideas
- Gradienboost started with an initial value (a single leaf, always can be a mean value), while adaboost started with a weak classifier
- new Tree was built to reduce the __Pseudo Residual__ of previous trees
  * Intial leaf -> calculate Residual
  * adding First Tree -> calculate Residual
- number of leafs can be 8 to 32
- using learning rate (e.g 0.1) to scale the contribution of a new tree

#### algorithm
Input data $${(x_{i})}$$
