import pytest
import numpy as np
from numpy.testing import assert_allclose

from keras.applications import imagenet_utils as utils


def test_preprocess_input():
    x = np.random.uniform(0, 255, (2, 3, 2, 3))
    assert utils.preprocess_input(x).shape == x.shape

    out1 = utils.preprocess_input(x, 'channels_last')
    out2 = utils.preprocess_input(np.transpose(x, (0, 3, 1, 2)), 'channels_first')
    assert_allclose(out1, out2.transpose(0, 2, 3, 1))


def test_decode_predictions():
    x = np.zeros((2, 1000))
    x[0, 372] = 1.0
    x[1, 549] = 1.0
    outs = utils.decode_predictions(x, top=1)
    scores = [out[0][2] for out in outs]
    assert scores[0] == scores[1]

    # the numbers of columns and ImageNet classes are not identical.
    with pytest.raises(ValueError):
        utils.decode_predictions(np.ones((2, 100)))


def test_obtain_input_shape():
    # input_shape and default_size are not identical.
    with pytest.raises(ValueError):
        utils._obtain_input_shape(
            input_shape=(224, 224, 3),
            default_size=299,
            min_size=139,
            data_format='channels_last',
            include_top=True)

    # Test invalid use cases
    for data_format in ['channels_last', 'channels_first']:
        # input_shape is smaller than min_size.
        shape = (100, 100)
        input_shape = shape + (3,) if data_format == 'channels_last' else (3,) + shape
        with pytest.raises(ValueError):
            utils._obtain_input_shape(
                input_shape=input_shape,
                default_size=None,
                min_size=139,
                data_format=data_format,
                include_top=False)

        # shape is 1D.
        shape = (100,)
        input_shape = shape + (3,) if data_format == 'channels_last' else (3,) + shape
        with pytest.raises(ValueError):
            utils._obtain_input_shape(
                input_shape=input_shape,
                default_size=None,
                min_size=139,
                data_format=data_format,
                include_top=False)

        # the number of channels is 5 not 3.
        shape = (100, 100)
        input_shape = shape + (5,) if data_format == 'channels_last' else (5,) + shape
        with pytest.raises(ValueError):
            utils._obtain_input_shape(
                input_shape=input_shape,
                default_size=None,
                min_size=139,
                data_format=data_format,
                include_top=False)

    assert utils._obtain_input_shape(
        input_shape=None,
        default_size=None,
        min_size=139,
        data_format='channels_last',
        include_top=False) == (None, None, 3)

    assert utils._obtain_input_shape(
        input_shape=None,
        default_size=None,
        min_size=139,
        data_format='channels_first',
        include_top=False) == (3, None, None)

    assert utils._obtain_input_shape(
        input_shape=None,
        default_size=None,
        min_size=139,
        data_format='channels_last',
        include_top=False) == (None, None, 3)

    assert utils._obtain_input_shape(
        input_shape=(150, 150, 3),
        default_size=None,
        min_size=139,
        data_format='channels_last',
        include_top=False) == (150, 150, 3)

    assert utils._obtain_input_shape(
        input_shape=(3, None, None),
        default_size=None,
        min_size=139,
        data_format='channels_first',
        include_top=False) == (3, None, None)


if __name__ == '__main__':
    pytest.main([__file__])
