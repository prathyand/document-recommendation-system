
import React from 'react';
import './App.css';
import ToggleSwitch from "./ToggleSwitch";
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import { handleRender } from './TooltipSlider'
import ColorToggleButton from './tglbtngrp';
import MenuListComposition from "./remindermenu"
import Stack from '@mui/material/Stack';
import Content from './readmore_abstract'

function Item(props) {
    const separateWords = s => s!=null?s.replace(/\<>/g, ', '):" "
    const formatDate = s => new Date(s).toLocaleDateString(undefined, { dateStyle: 'long' });
    return (
      <li className="item">
        <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={2}>
        <ToggleSwitch id={String(props.keyid)} checked={props.item.bookmarkflag} 
        onChange={() => props.handleChangeCheckbox(props.item.keyid,props.item.bookmarkflag)} />
        {(props.item.snooze_priority>-1) && <MenuListComposition keyid={props.item.keyid} setList={props.setList}
        setOpensnackbar={props.setOpensnackbar} setSnackbartext={props.setSnackbartext}></MenuListComposition>}
        </Stack>
        <h2 className="title">
          <a href={props.item.urllink} target="_blank" onClick={() => props.viewHandler(props.item.keyid,props.item.views)}>{props.item.title}</a>
        </h2>
        <p className="authors" style={{fontStyle: 'italic',marginTop: '10px'}} >
          <b>Authors:</b> {props.item.authors}
        </p>
  
        <p className="description">
        <Content key={props.item.keyid} text={props.item.descrptn}/>
        </p>
  
        <div className="meta">
          <span style={{fontSize: '16px', color:'green'}}>{formatDate(props.item.datemod)}</span>
          {
            <span style={{fontSize: '16px',color:'blue'}}>{separateWords(props.item.tags)}</span>
          }
          <span>
          <a  style={{fontSize: '15px'}} href="#" onClick={()=>props.LoadFeed(true,undefined,true,props.item.keyid)}>[View Similar]</a>
          </span>
        </div>
        <div>
        <Slider className='slidercss'
        min={-10} max={10}
        handleRender={handleRender}
        onAfterChange={(e)=>props.handleAfterChange(e,props.item.keyid)}
        onChange={(e)=>props.handleChangeRating(e,props.item.keyid)}
        defaultValue={props.item.rating} 
        value={props.item.rating}
        railStyle={{ backgroundColor: 'red', height: 10 }}
        trackStyle={{ backgroundColor: 'blue', height: 10 }}
        handleStyle={{
          // borderColor: 'blue',
          height: 28,
          width: 28,
          marginLeft: -14,
          marginTop: -9,
          backgroundColor: 'black',
        }}/>
        {(props.item.snooze_priority<=-1) &&
        <div className='rowC_snooze'>
          <p>Snooze for</p>
         <ColorToggleButton id={String(props.keyid)} onchangeevent={props.onChangesnooze} algnmnt={props.item.snoozeval_days===-1?undefined:props.item.snoozeval_days}></ColorToggleButton>
        </div>}
      </div>
      </li>
    );
  }

  export default Item