import argparse
import uff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_graph',
                        default='frozen_inference_graph.pb',
                        help='Frozen .pb graph to be converted')
    parser.add_argument('-o', '--output_graph',
                        default='frozen_inference_graph.uff',
                        help='Output .uff graph')
    args = parser.parse_args()

    _ = uff.from_tensorflow_frozen_model(args.input_graph,
                                         output_nodes=['NMS'],
                                         preprocessor='./preprocessor.py',
                                         output_filename=args.output_graph)


if __name__ == '__main__':
    main()
