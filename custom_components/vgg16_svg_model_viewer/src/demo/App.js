/* eslint no-magic-numbers: 0 */
import React, {Component} from 'react';

import {Matrix} from '../lib';

class App extends Component {
    constructor() {
        super();
        this.state = {
            value: '',
            selectedLayer: 36,
            hoverColor: 'blue',
        };
        this.setProps = this.setProps.bind(this);
    }

    setProps(newProps) {
        this.setState(newProps);
    }

    render() {
        return (
            <div>
                <Matrix setProps={this.setProps} {...this.state} />
            </div>
        );
    }
}

export default App;
