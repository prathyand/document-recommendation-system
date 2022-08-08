import React, { useState } from "react";
import "./App.css";

const ReadMore = ({ children }) => {
const text = children;
const [isReadMore, setIsReadMore] = useState(true);
const toggleReadMore = () => {
	setIsReadMore(!isReadMore);
};
return (
	<p style={{fontStyle: 'normal',fontSize: '16px',marginTop: '10px'}}>
	{isReadMore ? text.slice(0, 200) : text}
	<span onClick={toggleReadMore} className="read-or-hide">
		{isReadMore ? "...read more" : " show less"}
	</span>
	</p>
);
};

const Content = (props) => {
return (
		<ReadMore children={props.text}>
		</ReadMore>
);
};

export default Content;
