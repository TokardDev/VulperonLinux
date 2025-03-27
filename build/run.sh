#!/bin/bash

DISK_PATH="/tmp/vm_disk.qcow2"
VM_NAME="vulperon"
ISO_DIR="./"
ISO_PATH=$(ls -t "$ISO_DIR"/*.iso | head -n 1)

if [ -z "$ISO_PATH" ]; then
    echo "Aucun fichier ISO trouvé dans $ISO_DIR."
    exit 1
fi

echo "ISO le plus récent : $ISO_PATH"

if [ -f "$DISK_PATH" ]; then
    rm -f "$DISK_PATH"
fi

sudo qemu-img create -f qcow2 "$DISK_PATH" 10G

if sudo virsh dominfo "$VM_NAME" &>/dev/null; then
    echo "La VM existe déjà, suppression..."
    sudo virsh destroy "$VM_NAME" &>/dev/null
    sudo virsh undefine "$VM_NAME" &>/dev/null
fi

echo "Création et définition de la VM..."
cat <<EOF | sudo tee /etc/libvirt/qemu/$VM_NAME.xml > /dev/null
<domain type='kvm'>
  <name>$VM_NAME</name>
  <memory unit='KiB'>2097152</memory>
  <vcpu placement='static'>2</vcpu>
  <os>
    <type arch='x86_64' machine='q35'>hvm</type>
    <boot dev='cdrom'/>
  </os>
  <features>
    <acpi/>
    <apic/>
  </features>
  <clock offset='utc'/>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='$DISK_PATH'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <disk type='file' device='cdrom'>
      <driver name='qemu' type='raw'/>
      <source file='$ISO_PATH'/>
      <target dev='hdc' bus='ide'/>
      <readonly/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <graphics type='spice' autoport='yes'/>
    <input type='tablet' bus='usb'/>
  </devices>
</domain>
EOF

sudo virsh define /etc/libvirt/qemu/$VM_NAME.xml

echo "Démarrage de la VM $VM_NAME..."
sudo virsh start "$VM_NAME"

echo "La VM est en cours d'exécution. Ouvre virt-manager pour voir la console."
echo "Appuie sur [Entrée] pour l'arrêter."
read

echo "Arrêt de la VM..."
sudo virsh shutdown "$VM_NAME"
sleep 5

echo "Suppression du disque temporaire..."
sudo rm -f "$DISK_PATH"

echo "Processus terminé."
