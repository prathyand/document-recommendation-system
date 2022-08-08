import React from 'react';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

export default function ColorToggleButton({id,onchangeevent,algnmnt}) {
    // const [alignment, setAlignment] = React.useState(algnmnt);
    const handleChange = (event, newAlignment) => {
        // setAlignment(newAlignment);
        onchangeevent(id,newAlignment);
    };
    return (React.createElement(ToggleButtonGroup, { color: "success", value: algnmnt, exclusive: true, onChange: handleChange, size: 'small' },
        React.createElement(ToggleButton, { value: 2 }, "2days"),
        React.createElement(ToggleButton, { value: 7 }, "7days"),
        React.createElement(ToggleButton, { value: 14 }, "14days")));
}