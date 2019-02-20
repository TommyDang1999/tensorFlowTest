import tensorflow
from tensorflow import keras
import numpy
import matplotlib.pyplot as plotter
# this file is dedicated to jake

#lets check what version of tf we have
print("Tensorflow ver: ", tensorflow.__version__)

#let's import the fashion mnist
fashion_mnist = keras.datasets.fashion_mnist

#return four numpy arrays;
#train_ -> training set, test_ -> testing set
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

#class names are not included with the dataset, lets make them ourselves
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

#lets see how many images are in the training set and how big in width x height
print("train_images.shape: ", train_images.shape)

#lets see how many labels
print("train_labels: ", len(train_labels)) # len returns us the (len)gth


print("test_images.shape: ", test_images.shape) 

print("test_labels: ", len(test_labels))

#preprocess the data
plotter.figure()
plotter.imshow(train_images[0])
plotter.colorbar()
plotter.grid(False)
plotter.show()

#scale values from range 0 - 1
train_images = train_images / 255.0
test_images = test_images / 255.0

#display first 25 images from training set and display class name below each image
plotter.figure(figsize=(10, 10))
for i in range(25):
    plotter.subplot(5, 5, i + 1)
    plotter.xticks([])
    plotter.yticks([])
    plotter.grid(False)
    plotter.imshow(train_images[i], cmap=plotter.cm.binary)
    plotter.xlabel(class_names[train_labels[i]])
plotter.show()

#build the model

#setup layers

# The first layer in this network, tensorflow.keras.layers.Flatten, transforms the format of the images 
# from a 2d-array (of 28 by 28 pixels), to a 1d-array of 28 * 28 = 784 pixels. 
# Think of this layer as unstacking rows of pixels in the image and lining them up. 
# This layer has no parameters to learn; it only reformats the data.

# After the pixels are flattened, the network consists of a sequence of two tensorflow.keras.layers.Dense layers. 
# These are densely-connected, or fully-connected, neural layers. The first Dense layer has 128 nodes (or neurons). 
# The second (and last) layer is a 10-node softmax layer—this returns an array of 10 probability scores that sum to 1. 
# Each node contains a score that indicates the probability that the current image belongs to one of the 10 classes.

model = keras.Sequential([keras.layers.Flatten(input_shape=(28, 28)), keras.layers.Dense(128, activation=tensorflow.nn.relu), keras.layers.Dense(10, activation=tensorflow.nn.softmax)])



#compile the model

# Before the model is ready for training, it needs a few more settings. 
# These are added during the model's compile step:

# Loss function — This measures how accurate the model is during training. We want to minimize this function to "steer" the model in the right direction.
# Optimizer — This is how the model is updated based on the data it sees and its loss function.
# Metrics — Used to monitor the training and testing steps. The following example uses accuracy, the fraction of the images that are correctly classified.

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

#train the model

# Training the neural network model requires the following steps:

# 1. Feed the training data to the model—in this example, the train_images and train_labels arrays.
# 2. The model learns to associate images and labels.
# 3. We ask the model to make predictions about a test set—in this example, the test_images array. 
#    We verify that the predictions match the labels from the test_labels array.

# To start training, call the model.fit method—the model is "fit" to the training data:

model.fit(train_images, train_labels, epochs=5)

# As the model trains, the loss and accuracy metrics are displayed. 
# This model reaches an accuracy of about 0.88 (or 88%) on the training data.

#evaluate accuracy

test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test Accuracy: ', test_acc)

#make predictions

# With the model trained, we can use it to make predictions about some images.
predictions = model.predict(test_images)

#lets look at the first prediction
print('Prediction[0]', predictions[0])

#which label has the highest confidence value
print('Label with highest confidence value: ', numpy.argmax(predictions[0]))

#so we can check which label that is with class_name
print('Label with highest confidence value with class_name: ', class_names[numpy.argmax(predictions[0])])

#now we can check if this is correct
print('test_labels[0] = ', test_labels[0])

#if this is correct they will both be equal ^^

#now we can graph this to look at the full set
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plotter.grid(False)
  plotter.xticks([])
  plotter.yticks([])
  
  plotter.imshow(img, cmap=plotter.cm.binary)

  predicted_label = numpy.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'
  
  plotter.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*numpy.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plotter.grid(False)
  plotter.xticks([])
  plotter.yticks([])
  thisplot = plotter.bar(range(10), predictions_array, color="#777777")
  plotter.ylim([0, 1]) 
  predicted_label = numpy.argmax(predictions_array)
 
  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')


#0th image, predictions and prediction array
i = 0
plotter.figure(figsize=(6,3))
plotter.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
plotter.subplot(1,2,2)
plot_value_array(i, predictions,  test_labels)

#10th image, predictions, and prediction array
i = 10
plotter.figure(figsize=(6,3))
plotter.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
plotter.subplot(1,2,2)
plot_value_array(i, predictions,  test_labels)


# Plot the first X test images, their predicted label, and the true label
# Color correct predictions in blue, incorrect predictions in red
num_rows = 5
num_cols = 3
num_images = num_rows * num_cols
plotter.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
for i in range(num_images):
  plotter.subplot(num_rows, 2 * num_cols, 2 * i + 1)
  plot_image(i, predictions, test_labels, test_images)
  plotter.subplot(num_rows, 2 * num_cols, 2 * i + 2)
  plot_value_array(i, predictions, test_labels)


# now we can use the model to test any image from the test datasheet
img = test_images[0]

print('Image: ', img.shape)

# we need to add it to a list so we can use the optimizer, regardless of if its the only one
img = (numpy.expand_dims(img, 0))

print('Image: ', img.shape)


# now we can predict
predictions_single = model.predict(img)

print(predictions_single)

plot_value_array(0, predictions_single, test_labels)
_ = plotter.xticks(range(10), class_names, rotation=45)

print('Image predicted: ', numpy.argmax(predictions_single[0]))
print('Image predicted: ', class_names[numpy.argmax(predictions_single[0])])