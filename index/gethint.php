<?php
/**
 * Created by PhpStorm.
 * User: davidfnck
 * Date: 2017/7/18
 * Time: 下午12:48
 */

//get the q parameter from URL
$q=$_GET["q"];
//$q = 'i,i';

//全部小写化
$q=strtolower($q);

// 读取 config 文件,上传到 github 上面的是 config.example 文件，请注意
$configs = include('config.php');

//使用pdo连接数据库
$dbms = $configs['dbms'];     //数据库类型
$host = $configs['host']; //数据库主机名
$dbName = $configs['dbName'];    //使用的数据库
$user = $configs['user'];      //数据库连接用户名
$pass = $configs['pass'];     //对应的密码
$dsn = "$dbms:host=$host;dbname=$dbName";

try {
    $dbh = new PDO($dsn, $user, $pass);
    $dbh->query('set names utf8;');
} catch (PDOException $e) {
    echo "连接失败" . $e->getMessage();
}

//lookup all hints from array if length of q>0
if (strlen($q) > 0)
{
    // 这种数据库链接方案已经被弃用
    // $con = mysql_connect("localhost","root","6n2]E,(tUN4BqZDH$W/}$3>nM6rV#ze2GWft3Fg$8TDAj9bw4B");
    // if(!$con)
    // {
    //     die('Could not connect: ' .mysql_error());
    // }
    // mysql_select_db("ezrhyme_db",$con);

    // 老版本中读取 MySQL 的时候出现的字符编码问题，需要通过这个方式解决
    // $result =mysql_query('SET character_set_connection=utf8, character_set_results=utf8, character_set_client=binary',$con);

    $sql = "select * from ezrhyme_01";
    //$sql="SELECT FirstName FROM Persons where Firstname like '%$q%'";

    // $result =mysql_query($sql,$con);
    $result = $dbh->query($sql);


    $hint="";
    // while($row = mysql_fetch_array($result))
    while($row = $result->fetch())
    {

        # 匹配单押,双押
        if (strlen($q) == 1)
        {
            if (strtolower($q)==substr($row['single_rhyme'],-2,-1))
            {
                if ($hint=="")
                {
                    $hint=$row['word'];
                }
                else
                {
                    $hint=$hint." , ".$row['word'];
                }
            }
        }
        elseif (strlen($q) == 2)
        {
            if (strtolower($q)==substr($row['single_rhyme'],-3,-1))
            {
                if ($hint=="")
                {
                    $hint=$row['word'];
                }
                else
                {
                    $hint=$hint." , ".$row['word'];
                }
            }
        }
        else
        {
            if (strtolower($q)==substr($row['single_rhyme'],-4,-1))
            {
                if ($hint=="")
                {
                    $hint=$row['word'];
                }
                else
                {
                    $hint=$hint." , ".$row['word'];
                }
            }

        }
    }

}

//Set output to "no suggestion" if no hint were found
//or to the correct values
if ($hint == "")
{
    $response="oops……try again!";
}
else
{
    $response=$hint;
}

//output the response
echo $response;
?>
