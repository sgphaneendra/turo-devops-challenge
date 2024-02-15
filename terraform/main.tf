locals {
  deploy_yaml      = replace(file(var.deployment_yaml), "kube_namespace", var.kube_namespace)
  ssl_service_yaml = replace(file(var.ssl_service_yaml), "kube_namespace", var.kube_namespace)
  configmap_yaml = replace(file(var.configmap_yaml), "kube_namespace", var.kube_namespace)
  ingress_yaml = replace(file(var.ingress_yaml), "kube_namespace", var.kube_namespace)
}

resource "kubernetes_manifest" "turo-test-deployment" {
  manifest = yamldecode(replace(local.deploy_yaml, "docker_image_replace", var.image_name))

  wait {
    rollout = true
  }

  field_manager {
    # set the name of the field manager
    name = "sgphaneendra"
    # force field manager conflicts to be overridden
    force_conflicts = false
  }
}

resource "kubernetes_manifest" "ssl_service" {
  manifest = yamldecode(replace(local.ssl_service_yaml, "dns_name", var.dns_name))
  field_manager {
    # set the name of the field manager
    name = "sgphaneendra"
    # force field manager conflicts to be overridden
    force_conflicts = false
  }

}

resource "kubernetes_manifest" "ingress" {
  manifest = yamldecode(replace(local.ingress_yaml, "dns_name", var.dns_name))
  field_manager {
    # set the name of the field manager
    name = "sgphaneendra"
    # force field manager conflicts to be overridden
    force_conflicts = false
  }

}

resource "kubernetes_manifest" "configmap" {
    manifest = yamldecode(replace(local.configmap_yaml, "dns_name", var.dns_name))
    field_manager {
    # set the name of the field manager
    name = "sgphaneendra"
    # force field manager conflicts to be overridden
    force_conflicts = false
  }
}
