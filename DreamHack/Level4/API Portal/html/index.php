<?php

$action = $_GET["action"] ?? "main";

switch($action) {
    case "main":
        break;
    case "help":
        break;
    
    // Safe key-value DB API
    case "db/create":
        $param = array($_GET["key"]);
        break;
    case "db/list":
        break;
    case "db/delete":
        $param = array($_GET["key"]);
        break;
    case "db/save":
        $param = array($_GET["dbkey"], $_GET["key"], $_GET["value"]);
        break;
    case "db/read":
        $param = array($_GET["dbkey"], $_GET["key"]);
        break;

    // Network-related API
    case "net/proxy/get":
        $param = array($_GET["url"], $_SERVER["REMOTE_ADDR"], urldecode($_SERVER["REQUEST_URI"]));
        break;
    case "net/proxy/post":
        $param = array($_GET["url"], $_SERVER["REMOTE_ADDR"], urldecode($_SERVER["REQUEST_URI"])); //TODO: implement POST data
        break;
    case "net/ping":
        $param = array($_GET["target"]);
        break;
    case "net/nslookup":
        $param = array($_GET["domain"], $_GET["record"]);
        break;

    // For your treat
    case "cheat/read-file":
        $param = array($_GET["name"]);
        break;
    case "cheat/eval":
        $param = array($_GET["code"]);
        break;
    case "cheat/phpinfo":
        break;

    // Flag
    case "flag/flag":
        $param = array($_GET["flag"]);
        break;

    default:
        $action = "main";
        break;
}

include "action/$action.php";
