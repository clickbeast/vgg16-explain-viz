import React, {Component} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const colors = {
    highlight: '#007AFF',
};

const MatrixItem = (props) => {
    const {
        className,
        children,
        value,
        onMouseEnter,
        onMouseLeave,
        binary,
        layout,
        itemLayout,
    } = props;
    return (
        <React.Fragment>
            <td className={className}>
                <div onHover={() => console.log('kjsds')}>
                    <StyledBlankLink
                        href={'#'}
                        onMouseEnter={onMouseEnter}
                        onMouseLeave={onMouseLeave}
                    >
                        {layout.binary ? (
                            <StyledMatrixItemBinary {...props} />
                        ) : (
                            <StyledMatrixItemValue {...props}>
                                {value}
                            </StyledMatrixItemValue>
                        )}
                    </StyledBlankLink>
                </div>
            </td>
        </React.Fragment>
    );
};

const StyledMatrixItemBinary = styled.span`
    background: ${(props) =>
        props.highlight ? colors.highlight : props.background || 'translucent'};

    color: ${(props) => (props.highlight ? 'white' : props.color || 'black')};
    box-sizing: border-box;
    -moz-box-sizing: border-box;
    -webkit-box-sizing: border-box;
    height: 16px;
    width: 16px;
    border-radius: ${(props) =>
        props.layout.binaryShape === 'circle' ? '50%' : '0%'};
    display: inline-block;
    margin-left: 3px;
    margin-top: 2px;
    background-color: ${(props) => (props.value === 1 ? 'black' : 'white')};
    border: 1px solid
        ${(props) => {
            if (props.value === 0) {
                if (props.highlight) {
                    if (props.itemLayout) {
                        return props.itemLayout.background || colors.highlight;
                    }
                    return colors.highlight;
                }

                if (props.itemLayout) {
                    if (props.itemLayout.highlight) {
                        if (props.itemLayout.background) {
                            return props.itemLayout.background;
                        }
                        return colors.highlight;
                    }
                }

                return 'black';
            }

            return 'translucent';
        }};

    background: ${(props) => {
        if (props.value === 1) {
            if (props.highlight) {
                if (props.itemLayout) {
                    return props.itemLayout.background || colors.highlight;
                }
                return colors.highlight;
            }

            if (props.itemLayout) {
                if (props.itemLayout.highlight) {
                    if (props.itemLayout.background) {
                        return props.itemLayout.background;
                    }
                    return colors.highlight;
                }
            }
            return 'black';
        }
        return 'white';
    }};

    text-decoration: none;
`;

const StyledMatrixItemValue = styled.div`
    text-decoration: none;
`;

const StyledBlankLink = styled.a`
    text-decoration: none;
    color: black;
    &:hover ${StyledMatrixItemValue} {
        background: ${colors.highlight};
        color: white;
    }
    &:hover ${StyledMatrixItemBinary} {
        background: ${colors.highlight};
        color: white;
    }
`;

const StyledMatrixItem = styled(MatrixItem)``;

const TopItem = ({className, children, value}) => (
    <React.Fragment>
        <td className={className} style={{textAlign: 'center'}}>
            {value}
        </td>
    </React.Fragment>
);

const StyledTopItem = styled(TopItem)`
    color: ${(props) => props.color || 'black'};
    background: ${(props) => props.background || 'lightGray'};
    border-radius: ${(props) => (props.shape === 'circle' ? '50%' : '50%')};

    height: 16px;
    width: 16px;
    line-height: 16px;
    padding: 4px;

    ${(props) => {
        if (props.highlight) {
            return 'background:' + colors.highlight + '; color:white';
        }
    }}
`;

const LeftItem = (props) => {
    const {i, className, value} = props;
    return <div className={className}> {value} </div>;
};

const StyledLeftItem = styled(LeftItem)`
    color: ${(props) => props.color || 'black'};
    background: ${(props) => props.background || 'lightGray'};
    border-radius: ${(props) => (props.shape === 'circle' ? '50%' : '0')};
    text-align: center;
    padding: 4px;
    height: 16px;
    width: 16px;
    line-height: 16px;
    margin-left: auto;

    ${(props) => {
        if (props.highlight) {
            return 'background:' + colors.highlight + '; color:white';
        }
    }}
`;

const LeftHeaderElement = (props) => {
    return <td></td>;
};

const extractValueFromLeftData = (data, i) => {
    if (data.left.data.length > 0) {
        return data.left.data[i];
    }
};

const Table = styled.table`
    border-spacing: 5px 4px;
    padding-top: ${(props) => {
        if (props.data.right.data) {
            if (props.data.right.data.length > 0) {
                return '40px';
            }
        }
        return '0px';
    }};

    padding-right: ${(props) => {
        if (props.data.right.data) {
            if (props.data.right.data.length > 0) {
                return '60px';
            }
        }

        return '0px';
    }};
`;

const Content = styled.div``;

const Item = ({className, children}) => {
    return (
        <td className={className}>
            <div className="content">{children}</div>
        </td>
    );
};

const StyledItem = styled(Item)`
    .content {
        text-align: center;
        color: ${(props) => props.layout.color || 'black'};
        font-family: 'Open Sans', 'HelveticaNeue', 'Helvetica Neue', Helvetica,
            Arial, sans-serif;
        vertical-align: center;
        line-height: 16px;
    }
`;

const HeaderItemBottom = ({className, children}) => {
    return (
        <th className={className}>
            <div className="content">{children}</div>
        </th>
    );
};

const StyledHeaderItemBottom = styled(HeaderItemBottom)`
    margin-left: auto;
    text-align: right;
    .content {
        color: ${(props) => props.layout.color || 'black'};
    }
`;

const HeaderItemRight = ({className, children}) => {
    return (
        <th className={className}>
            <div className="content">{children}</div>
        </th>
    );
};

const StyledHeaderItemRight = styled(HeaderItemRight)`
    margin-left: auto;
    text-align: right;

    .content {
        color: ${(props) => props.layout.color || 'black'};
        transform: rotate(-45deg);
        position: absolute;
        margin-top: -30px;
        margin-left: -5px;
    }
`;

const DoubleRect = ({className, children}) => {
    return (
        <div className={className}>
            <div className="content">{children}</div>
        </div>
    );
};
const StyledDoubleRect = styled(DoubleRect)`
    width: 50px;
    height: 50px;
    margin-left: 100px;
    position: relative;
    background: ${colors.primBlue};
    overflow: hidden;
    color: white;

    text-align: center;
    vertical-align: middle;
    line-height: 50px;

    :before {
        width: 100%;
        height: 50%;
        position: absolute;
        content: '';
        top: 50%;
        background: ${colors.primGreen};
        left: 0px;
    }

    .content {
        position: absolute;
        width: 100%;
        height: 100%;
    }
`;

export default class MatrixOld extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {
            enteredItem: {
                i: -1,
                j: -1,
            },
        };
    }

    setEnteredItemState(set, i, j) {
        if (set) {
            this.setState({
                enteredItem: {
                    i: i,
                    j: j,
                },
            });
        } else {
            this.setState({
                enteredItem: {
                    i: -1,
                    j: -1,
                },
            });
        }
    }

    render() {
        const {id, setProps, data} = this.props;

        return (
            <div>
                <h1>WHATS UP WORLD</h1>
                <svg width="802px" height="130px" viewBox="0 0 802 130">
                    <title>VGG-16-Visualization.drawio(6)</title>
                    <g
                        id="Page-3"
                        stroke="none"
                        strokeWidth="1"
                        fill="none"
                        fillRule="evenodd"
                    >
                        <g
                            id="Artboard"
                            transform="translate(1.000000, -48.000000)"
                        >
                            <g
                                id="VGG-16-Visualization.drawio(6)"
                                transform="translate(0.000000, 49.000000)"
                            >
                                <g
                                    id="layer_32"
                                    transform="translate(658.858859, 57.285285)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 29.4294294 10.2882883 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 4.2042042 4.2042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 4.2042042 4.2042042 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <path
                                        d="M4.2042042,10.2882883 L4.2042042,4.2042042 L0,0 M4.2042042,4.2042042 L29.4294294,4.2042042"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_29"
                                    transform="translate(569.969970, 44.522523)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_28"
                                    transform="translate(562.162162, 44.372372)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_27"
                                    transform="translate(539.939940, 44.372372)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_26"
                                    transform="translate(532.132132, 44.222222)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_13"
                                    transform="translate(294.894895, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_12"
                                    transform="translate(287.087087, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_11"
                                    transform="translate(264.864865, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_3"
                                    transform="translate(89.489489, 0.192192)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 128.078078 12.012012 128.078078 0 116.066066"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 128.078078 0 116.066066"
                                    ></polygon>
                                    <path
                                        d="M12.012012,128.078078 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_20"
                                    transform="translate(416.816817, 36.600601)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_6"
                                    transform="translate(162.762763, 12.240240)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 18.018018 94.966967 12.012012 94.966967 0 82.954955"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 12.012012 12.012012 12.012012 94.966967 0 82.954955"
                                    ></polygon>
                                    <path
                                        d="M12.012012,94.966967 L12.012012,12.012012 L0,-2.13376197e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_25"
                                    transform="translate(509.909910, 44.372372)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_5"
                                    transform="translate(154.954955, 12.240240)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 18.018018 94.966967 12.012012 94.966967 0 82.954955"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 12.012012 12.012012 12.012012 94.966967 0 82.954955"
                                    ></polygon>
                                    <path
                                        d="M12.012012,94.966967 L12.012012,12.012012 L0,-2.13376197e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_10"
                                    transform="translate(257.057057, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_19"
                                    transform="translate(409.009009, 36.600601)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_24"
                                    transform="translate(502.102102, 44.222222)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_30"
                                    transform="translate(600.000000, 54.132132)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#9B5B58"
                                        fill="#61403E"
                                        fillRule="nonzero"
                                        points="0 0 11.4114114 0 17.4174174 6.00600601 17.4174174 16.3003003 6.00600601 16.3003003 0 10.2942943"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 11.4114114 0 17.4174174 6.00600601 6.00600601 6.00600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 6.00600601 6.00600601 16.3003003 0 10.2942943"
                                    ></polygon>
                                    <path
                                        d="M6.00600601,16.3003003 L6.00600601,6.00600601 L0,0 M6.00600601,6.00600601 L17.4174174,6.00600601"
                                        id="Shape"
                                        stroke="#9B5B58"
                                    ></path>
                                </g>
                                <g
                                    id="layer_23"
                                    transform="translate(481.081081, 44.222222)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#9B5B58"
                                        fill="#61403E"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 33.033033 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 33.033033 0 21.021021"
                                    ></polygon>
                                    <path
                                        d="M12.012012,33.033033 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#9B5B58"
                                    ></path>
                                </g>
                                <g
                                    id="layer_31"
                                    transform="translate(631.831832, 57.285285)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#46702E"
                                        fill="#344333"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 29.4294294 10.2882883 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 4.2042042 4.2042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 4.2042042 4.2042042 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <path
                                        d="M4.2042042,10.2882883 L4.2042042,4.2042042 L0,0 M4.2042042,4.2042042 L29.4294294,4.2042042"
                                        id="Shape"
                                        stroke="#46702E"
                                    ></path>
                                </g>
                                <g
                                    id="layer_35"
                                    transform="translate(754.954955, 57.285285)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#46702E"
                                        fill="#344333"
                                        fillRule="nonzero"
                                        points="0 0 13.8138138 0 18.018018 4.2042042 18.018018 10.2882883 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 13.8138138 0 18.018018 4.2042042 4.2042042 4.2042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 4.2042042 4.2042042 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <path
                                        d="M4.2042042,10.2882883 L4.2042042,4.2042042 L0,0 M4.2042042,4.2042042 L18.018018,4.2042042"
                                        id="Shape"
                                        stroke="#46702E"
                                    ></path>
                                </g>
                                <g
                                    id="layer_output"
                                    transform="translate(781.981982, 57.141141)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#A3B0D7"
                                        fill="#50516D"
                                        fillRule="nonzero"
                                        points="0 0 13.8138138 0 18.018018 4.2042042 18.018018 10.2882883 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 13.8138138 0 18.018018 4.2042042 4.2042042 4.2042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 4.2042042 4.2042042 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <path
                                        d="M4.2042042,10.2882883 L4.2042042,4.2042042 L0,0 M4.2042042,4.2042042 L18.018018,4.2042042"
                                        id="Shape"
                                        stroke="#A3B0D7"
                                    ></path>
                                </g>
                                <g
                                    id="layer_8"
                                    transform="translate(192.792793, 12.240240)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 18.018018 96.018018 12.012012 96.018018 0 84.006006"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 12.012012 12.012012 12.012012 96.018018 0 84.006006"
                                    ></polygon>
                                    <path
                                        d="M12.012012,96.018018 L12.012012,12.012012 L0,-2.13376197e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_7"
                                    transform="translate(184.984985, 12.240240)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 18.018018 96.018018 12.012012 96.018018 0 84.006006"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 12.012012 12.012012 12.012012 96.018018 0 84.006006"
                                    ></polygon>
                                    <path
                                        d="M12.012012,96.018018 L12.012012,12.012012 L0,-2.13376197e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_4"
                                    transform="translate(131.531532, 12.240240)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#9B5B58"
                                        fill="#61403E"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 18.018018 96.018018 12.012012 96.018018 0 84.006006"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 6.00600601 -2.13376197e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -2.13376197e-15 12.012012 12.012012 12.012012 96.018018 0 84.006006"
                                    ></polygon>
                                    <path
                                        d="M12.012012,96.018018 L12.012012,12.012012 L0,-2.13376197e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#9B5B58"
                                    ></path>
                                </g>
                                <g
                                    id="layer_2"
                                    transform="translate(81.681682, 0.192192)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 128.078078 12.012012 128.078078 0 116.066066"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 128.078078 0 116.066066"
                                    ></polygon>
                                    <path
                                        d="M12.012012,128.078078 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_22"
                                    transform="translate(446.846847, 38.258258)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 4.26752394e-15 6.00600601 4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 4.26752394e-15 6.00600601 4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_21"
                                    transform="translate(439.039039, 38.258258)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 4.26752394e-15 6.00600601 4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 4.26752394e-15 6.00600601 4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_18"
                                    transform="translate(386.786787, 36.600601)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_17"
                                    transform="translate(378.978979, 36.600601)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_1"
                                    transform="translate(59.459459, 0.192192)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 126.054054 12.012012 126.054054 0 114.042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 126.054054 0 114.042042"
                                    ></polygon>
                                    <path
                                        d="M12.012012,126.054054 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_0"
                                    transform="translate(51.651652, 0.192192)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 18.018018 126.054054 12.012012 126.054054 0 114.042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 6.00600601 0 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 12.012012 12.012012 12.012012 126.054054 0 114.042042"
                                    ></polygon>
                                    <path
                                        d="M12.012012,126.054054 L12.012012,12.012012 L0,0 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_9"
                                    transform="translate(235.435435, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#9B5B58"
                                        fill="#61403E"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#9B5B58"
                                    ></path>
                                </g>
                                <g
                                    id="layer_16"
                                    transform="translate(356.156156, 36.600601)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#9B5B58"
                                        fill="#61403E"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 48.048048 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 48.048048 0 36.036036"
                                    ></polygon>
                                    <path
                                        d="M12.012012,48.048048 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#9B5B58"
                                    ></path>
                                </g>
                                <g id="layer_input">
                                    <polygon
                                        id="Path"
                                        stroke="#BDA1C8"
                                        fill="#543B5E"
                                        fillRule="nonzero"
                                        points="0 -4.10082378e-15 6.00600601 -4.10082378e-15 18.018018 12.012012 18.018018 126.054054 12.012012 126.054054 0 114.042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.10082378e-15 6.00600601 -4.10082378e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.10082378e-15 12.012012 12.012012 12.012012 126.054054 0 114.042042"
                                    ></polygon>
                                    <path
                                        d="M12.012012,126.054054 L12.012012,12.012012 L0,-4.10082378e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#BDA1C8"
                                    ></path>
                                </g>
                                <g
                                    id="layer_34"
                                    transform="translate(720.120120, 57.285285)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 29.4294294 10.2882883 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 4.2042042 4.2042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 4.2042042 4.2042042 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <path
                                        d="M4.2042042,10.2882883 L4.2042042,4.2042042 L0,0 M4.2042042,4.2042042 L29.4294294,4.2042042"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_33"
                                    transform="translate(693.093093, 57.285285)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#46702E"
                                        fill="#344333"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 29.4294294 10.2882883 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 25.2252252 0 29.4294294 4.2042042 4.2042042 4.2042042"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 0 4.2042042 4.2042042 4.2042042 10.2882883 0 6.08408408"
                                    ></polygon>
                                    <path
                                        d="M4.2042042,10.2882883 L4.2042042,4.2042042 L0,0 M4.2042042,4.2042042 L29.4294294,4.2042042"
                                        id="Shape"
                                        stroke="#46702E"
                                    ></path>
                                </g>
                                <g
                                    id="layer_15"
                                    transform="translate(324.324324, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#885A00"
                                        fill="#36210A"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#885A00"
                                    ></path>
                                </g>
                                <g
                                    id="layer_14"
                                    transform="translate(316.516517, 23.687688)"
                                >
                                    <polygon
                                        id="Path"
                                        stroke="#6580A8"
                                        fill="#313C4B"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 18.018018 72.0720721 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.05"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 6.00600601 -4.26752394e-15 18.018018 12.012012 12.012012 12.012012"
                                    ></polygon>
                                    <polygon
                                        id="Path"
                                        fillOpacity="0.1"
                                        fill="#000000"
                                        fillRule="nonzero"
                                        points="0 -4.26752394e-15 12.012012 12.012012 12.012012 72.0720721 0 60.0600601"
                                    ></polygon>
                                    <path
                                        d="M12.012012,72.0720721 L12.012012,12.012012 L0,-4.26752394e-15 M12.012012,12.012012 L18.018018,12.012012"
                                        id="Shape"
                                        stroke="#6580A8"
                                    ></path>
                                </g>
                            </g>
                        </g>
                    </g>
                </svg>
            </div>
        );
    }
}

MatrixOld.defaultProps = {};

MatrixOld.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The data that needs to be displayed
     */

    data: PropTypes.object,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,
};
