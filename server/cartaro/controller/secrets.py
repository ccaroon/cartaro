from cartaro.model.secret import Secret
import cartaro.controller.base as base

secrets = base.create_controller("secrets", Secret)
