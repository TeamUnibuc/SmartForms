import { Switch } from "@mui/material"
import React from "react"

interface HeaderProps
{
  themeChanger: React.Dispatch<React.SetStateAction<boolean>>
  isDarkTheme: boolean
}

export default function Header(props: HeaderProps): JSX.Element
{
  const switchClicked = () => {
    props.themeChanger(!props.isDarkTheme)
  }

  return <>
    <Switch checked={props.isDarkTheme} onChange={switchClicked} />
  </>
}
