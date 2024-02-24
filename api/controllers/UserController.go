package controllers

import "github.com/gin-gonic/gin"

type UserController struct{}

func (u UserController) Login(c *gin.Context) {}

func (u UserController) Register(c *gin.Context) {}

func (u UserController) Get(c *gin.Context) {}
