import './App.css';
import Tabs from "./components/Tabs";
import { saveAs } from 'file-saver'
import React, { useState, useEffect } from "react";

function App() {
  const [myValue, setMyValue]=useState('')

  const [myResult, setMyResult]=useState('')

  const createFile = () => {
    const blob = new Blob([ myValue ], { type: 'text/plain;charset=utf-8' })
    saveAs(blob, 'mi-archivo.txt')
  }

  const readFile = ( e ) => {
      const file = e.target.files[0]

      if( !file ) return

      const fileReader = new FileReader()

      fileReader.readAsText( file )
      
      fileReader.onload = () => {
        setMyValue ( fileReader.result )

      }
      
      fileReader.onerror = () => {
        setMyValue ( fileReader.error )
      }
    }

    function handleCompile() {
      return fetch('/compile', {
          method: 'POST',
          credentials: 'include',
          headers: { 'Accept': 'application/json', "Content-Type": "application/json" },
          body: JSON.stringify({"code": myValue})
       }).then(response => response.json().then(data=>setMyResult(data.code)))
         .catch(error => console.log(error))
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>PyToPy Compiler</h1>                        
      </header>
        <Tabs>
        <div label="Home">
          <p>Grupo 12</p>    
        </div>
        <div label="Editor">
          <div className="container">
                      <button className="button" style={{"marginLeft": "10px"}} onClick={ createFile } >
                        Guardar archivo
                      </button>
                      <button className="button"  style={{"marginLeft": "5px"}} onClick={ handleCompile } >
                        Compilar
                      </button>  
                      <button className="button" style={{"marginLeft": "5px"}}  >
                        Optimizar por Mirilla
                      </button>
                      <button className="button" style={{"marginLeft": "5px"}} >
                        Optimizar por Bloques
                      </button>
          </div>
          <div className="container">
              <div className="box">               
                  <div className="box-row">
                      <div className="box-cell box1">
                        <textarea cols="89" rows="15" 
                        placeholder='Ingrese el código a analizar' 
                        value={ myValue }
                        onChange={ ( e ) => setMyValue( e.target.value ) }
                        ></textarea>
                      </div>
                      <div className="box-cell box2">
                        <textarea cols="89" rows="15" 
                        placeholder='Resultado de compilación' 
                        value={ myResult }
                        onChange={ ( e ) => setMyResult( e.target.value ) }
                        ></textarea>
                      </div>
                  </div>
              </div>
          </div> 
          <div className="open-file button" style={{"marginLeft": "10px"}}>
            <input type="file" onChange={ readFile } >          
            </input>
          </div>  
        </div>
        <div label="Reports">
        <div className="container">
                      <button className="button" style={{"marginLeft": "10px"}} >
                        Tabla de Símbolos
                      </button>
                      <button className="button"  style={{"marginLeft": "5px"}} >
                        Tabla de Errores
                      </button>  
                      <button className="button" style={{"marginLeft": "5px"}}  >
                        Optimización
                      </button>
                      <button className="button" style={{"marginLeft": "5px"}} >
                        Optimizar por Bloques
                      </button>
          </div>
          <br />
          <div className="report-container">

          </div>
        </div>
      </Tabs> 
    </div>
  );
}

export default App;
