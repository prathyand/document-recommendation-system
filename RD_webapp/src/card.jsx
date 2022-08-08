import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import Stack from '@mui/material/Stack';
// import CardHeader from '@mui/material/CardHeader';
// import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
// import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
// import { red } from '@mui/material/colors';
import SettingsIcon from '@mui/icons-material/Settings';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
// import MoreVertIcon from '@mui/icons-material/MoreVert';
import TagsInput from "./TagsInput"
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};

const ExpandMore = styled((props) => {
    const { expand } = props, other = __rest(props, ["expand"]);
    return React.createElement(IconButton, Object.assign({}, other));
})(({ theme, expand }) => ({
    transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
    }),
}));
export default function RecipeReviewCard() {
    const [expanded, setExpanded] = React.useState(false);
    const handleExpandClick = () => {
        setExpanded(!expanded);
    };
    return (React.createElement(Card, { sx: { maxWidth: 2000 } },
     
        React.createElement(CardActions, { disableSpacing: true },
           
                <Stack direction="row" alignItems="center" gap={1}>
          <SettingsIcon />
          <Typography variant="body1">User Preferences</Typography></Stack>,
            React.createElement(ExpandMore, { expand: expanded, onClick: handleExpandClick, "aria-expanded": expanded, "aria-label": "show more" },
                React.createElement(ExpandMoreIcon, null))),
        React.createElement(Collapse, { in: expanded, timeout: "auto", unmountOnExit: true },
            React.createElement(CardContent, null,
                <TagsInput></TagsInput>))));
}