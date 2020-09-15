nums = [6,11,7,9,4,2,1]

l = len(nums)
# for i in range(l-1):
#     if nums[i] > nums[i+1]:
#         tmp=nums[i]
#         nums[i]=nums[i+1]
#         nums[i+1] = tmp

for i in range(l-1):
    if nums[i] > nums[i+1]:
        nums[i],nums[i+1]=nums[i+1],nums[i]

print(nums)



