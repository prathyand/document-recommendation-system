import './Button.css';
const Button = ({color = "blue",name = "name",size = "medium",type = null,onClick}) => {
const onButtonClick = () => {
 if(onClick){
  onClick(name);
 }
}
return(
 <div className="button-container">
  <button className={`custom-button ${color} ${size} ${type}`} onClick={onButtonClick}>{name}</button>
 </div>
)
}
export default Button;